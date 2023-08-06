import select
import time


from nsj_sql_utils_lib.dbadapter3 import DBAdapter3
from nsj_sql_utils_lib.dbconection_psycopg2 import DBConnectionPsycopg2

from nsj_queue_lib.exception import NotFoundException
from nsj_queue_lib.lock_dao import LockDAO
from nsj_queue_lib.retry_util import RetryUtil
from nsj_queue_lib.tarefa_dao import TarefaDAO
from nsj_queue_lib.settings import (
    DB_HOST,
    DB_PORT,
    DB_BASE,
    DB_USER,
    DB_PASS,
    QUEUE_NAME,
    GLOBAL_RUN,
    QUEUE_MAX_RETRY,
    logger,
)


class MainThread:
    def __init__(self, worker):
        self.worker = worker

    def run(self):
        """
        Método de entrada da Thread, reponsável pelo loop infinito,
        e por abrir conexão com o BD.
        """
        logger.info("Thread de principal iniciada.")
        while GLOBAL_RUN:
            try:
                with DBConnectionPsycopg2(
                    DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                ) as dbconn:
                    self._run_wait_notify(dbconn.conn)
            except Exception as e:
                logger.exception(f"Erro desconhecido: {e}", e, stack_info=True)
                logger.info(
                    "Aguardando 5 segundos, para tentar nova conexão com o banco de dados."
                )
                time.sleep(5)

        logger.info("Thread de principal finalizada.")

    def _run_wait_notify(self, conn):
        """
        Lógica de ouvinte das notificações do BD.
        """

        # Como a variável é escrita, neste escopo, é preciso declarar que estamos usando
        # a mesma variável definida fora do escopo
        global GLOBAL_RUN

        with conn.cursor() as curs:
            curs.execute(f"LISTEN {QUEUE_NAME}")

            logger.info(f"Esperando notificações na fila.")
            while GLOBAL_RUN:
                if select.select([conn], [], [], 5) == ([], [], []):
                    logger.debug(
                        "Timeout - Na espera de dados do descritor de arquivo que representa a conexão com o BD. Estratégia para evitar espera ocupada."
                    )
                else:
                    conn.poll()
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        logger.info(
                            f"NOTIFY - Notificação recebida. PID: {notify.pid} CHANNEL: {notify.channel} PAYLOAD: {notify.payload}"
                        )

                        # Desligando o worker, caso seja notificado para desligamento
                        if notify.payload == "HALT":
                            GLOBAL_RUN = False

                        # Tentando executar alguma tarefa da fila
                        self._run_tarefas(conn)

    def _run_tarefas(self, conn):
        """
        Recupera a lista de tarefas pendentes, e tenta executar uma de cada vez.
        """

        db = DBAdapter3(conn)
        lock_dao = LockDAO(db)
        tarefa_dao = TarefaDAO(db)

        # Recuperando todas as tarefas pendentes
        logger.info("Recuperando tarefas pendentes.")
        pendentes, count = tarefa_dao.list_pendentes(QUEUE_MAX_RETRY)
        logger.info(f"Quantidade recuperada {count}.")

        for tarefa in pendentes:
            # Tentando pegar uma tarefa para trabalhar
            locked = False
            try:
                if not lock_dao.try_lock(tarefa["id"]):
                    logger.debug(
                        f"Desisitindo da tarefa com ID {tarefa['id']}. Pois já estava sendo executada em outro worker."
                    )
                    continue
                else:
                    locked = True

                # Recuperando a tarefa em si
                try:
                    tarefa = tarefa_dao.get(tarefa["id"])
                except NotFoundException as e:
                    logger.exception(
                        f"Tarefa com ID {tarefa['id']} excluída indevidamente do BD.",
                        e,
                        stack_info=True,
                    )
                    continue

                # Verificando se a tarefa ainda está pendente
                if tarefa["status"] != "pendente":
                    logger.debug(
                        f"Desisitindo da tarefa com ID {tarefa['id']}. Pois já havia sido pega para execução por outro worker."
                    )
                    continue

                # Tarefa pronta para trabalhar
                # TODO Refatorar para iniciar a tarefa em outra thread,
                # controlando o máximo de tarefas simultâneas,
                # por meio de uma configuração
                logger.info(f"Tarefa selecionada para trabalhar. ID: {tarefa['id']}")
                self._run_tarefa(tarefa_dao, tarefa)

            finally:
                if locked:
                    lock_dao.unlock(tarefa["id"])

    def _run_tarefa(self, dao: TarefaDAO, tarefa: dict[str, any]):
        """
        Trata da execução de uma tarefa específica, porém cuidando apenas dos status
        processando e falha.

        Este método invoca o _run_worker, o qual de fato dispara o código customizado.
        """

        logger.info(f"Iniciando execução da tarefa com  ID: {tarefa['id']}")

        # Atualizando status da tarefa para processando.
        logger.debug(
            f"Atualizando status da tarefa com ID: {tarefa['id']}, para processando."
        )
        dao.update_status(tarefa["id"], "processando")

        try:
            self._run_worker(tarefa)
        except Exception as e:
            logger.exception(
                f"Erro executando a tarefa com ID: {tarefa['id']}.", e, stack_info=True
            )

            RetryUtil().reenfileir_tarefa(dao, tarefa, False, str(e))

    def _run_worker(self, tarefa: dict[str, any]):
        """
        Executa de fato o código do worker, para tratar uma tarefa. Passos:
        1. Abre nova conexão com o BD
        2. Abre nova transação
        3. Se tiver sucesso, commita e atualiza o status para sucesso
        4. Se tiver falha, faz rollback (mas, o status para falha dependerá do método
        anterior, que chama este, porque o controle de falha se dá na conexão da MainThread)
        """

        # Iniciando nova conexão com o BD, para a tarefa
        with DBConnectionPsycopg2(
            DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
        ) as new_dbconn:
            new_db = DBAdapter3(new_dbconn.conn)
            new_dao = TarefaDAO(new_db)

            # Iniciando transação
            new_dao.db.begin()
            try:
                # Invocando o código customizado para execução da tarefa.
                self.worker.execute(tarefa, new_dbconn)

                # Atualizando o status para concluido com sucesso.
                logger.debug(
                    f"Atualizando status da tarefa com ID: {tarefa['id']}, para concluido com sucesso."
                )
                new_dao.update_status(tarefa["id"], "sucesso")

                # Comitando as alterações
                new_dao.db.commit()
            finally:
                # Fazendo rollback (que não terá efeito,
                # se já tiver sido feito commit)
                new_dao.db.rollback()
