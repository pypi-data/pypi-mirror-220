import time
import threading

from datetime import datetime
from typing import Any

from nsj_sql_utils_lib.dbconection_psycopg2 import DBConnectionPsycopg2
from nsj_sql_utils_lib.dbadapter3 import DBAdapter3

from nsj_queue_lib.lock_dao import LockDAO
from nsj_queue_lib.retry_util import RetryUtil
from nsj_queue_lib.tarefa_dao import TarefaDAO
from nsj_queue_lib.settings import (
    DB_HOST,
    DB_PORT,
    DB_BASE,
    DB_USER,
    DB_PASS,
    QUEUE_MINUTE_RETRY_THREAD,
    GLOBAL_RUN,
    logger,
)


class RetryThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        Roda um loop de reinserção das tentativas que falharam.

        A thread só roda de fato nos minutos configurados na
        variável de ambiente: QUEUE_MINUTE_RETRY_THREAD (com
        valor padrão: 0,5,10,15,20,25,30,35,40,45,50,55).

        Além disso, é pego um lock no BD, para que apenas um
        worker realize essa operação por vez (para não
        sobrecarregar o banco).
        """

        logger.info("Thread de retentativas iniciada.")
        while GLOBAL_RUN:
            # Aguardando 15 segundos a cada verificação se deve rodar
            time.sleep(15)
            logger.debug("Nova verificação da thread de retry")

            # Recuperando o minuto atual
            now = datetime.now()
            if not (str(now.minute) in QUEUE_MINUTE_RETRY_THREAD.split(",")):
                continue

            logger.debug("Vai iniciar, de fato, a thread de retry")

            # Realizando de fato a lógica de execução
            try:
                with DBConnectionPsycopg2(
                    DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                ) as dbconn:
                    db = DBAdapter3(dbconn.conn)
                    lock_dao = LockDAO(db)

                    lock = False
                    try:
                        if lock_dao.try_lock_retry():
                            lock = True
                        else:
                            logger.debug(
                                "Desistindo da thread de retentativas, porque já há outro worker operando o mesmo."
                            )
                            continue

                        logger.info("Iniciando tratamento de retentativas...")

                        tarefa_dao = TarefaDAO(db)
                        # self._retry_falhas(tarefa_dao)
                        self._retry_perdidas(tarefa_dao, lock_dao)

                    finally:
                        if lock:
                            lock_dao.unlock_retry()
            except Exception as e:
                logger.exception(f"Erro desconhecido: {e}", e, stack_info=True)
                logger.info(
                    "Aguardando 5 segundos, para tentar nova conexão com o banco de dados."
                )
                time.sleep(5)

        logger.info("Thread de retentativas finalizada.")

    # def _retry_falhas(self, tarefa_dao: TarefaDAO):
    #     """
    #     Reenfilera as tarefas que sofreram falha, mas carecem de nova tentativa.
    #     """

    #     # Recuperando lista de tarefas a reenfileirar
    #     reefileirar, count = tarefa_dao.get_recuperacao_falhas(QUEUE_MAX_RETRY)
    #     logger.info("Quantidade de tarefas a reenfileirar: {count}.")

    #     # Tratando cada tarefa
    #     for item in reefileirar:
    #         id_inicial = item["id_inicial"] or item["id"]
    #         logger.info(
    #             f"Reenfileirando a tarefa de id: {item['id']} e id_inicial: {id_inicial}."
    #         )

    #         self._reenfileir_tarefa(tarefa_dao, item)

    def _retry_perdidas(self, tarefa_dao: TarefaDAO, lock_dao: LockDAO):
        """
        Reenfilera as tarefas que se perdaram em status 'processando'
        """

        # Recuperando lista de tarefas a reenfileirar
        processando, count = tarefa_dao.list_recuperacao_processando()
        logger.info(f"Quantidade de tarefas pendentes, a verificar: {count}.")

        # Tratando cada tarefa
        for item in processando:
            id_inicial = item["id_inicial"] or item["id"]

            # Tentando pegar o lock da tarefa (não pode ser possível,
            # se estiver de fato em processamento):
            locked = False
            try:
                if not lock_dao.try_lock(item["id"]):
                    # Tarefa em processamento, não precisa fazer nada.
                    continue
                else:
                    logger.info(
                        f"Reenfileirando a tarefa de id: {item['id']} e id_inicial: {id_inicial}."
                    )
                    locked = True

                    RetryUtil().reenfileir_tarefa(tarefa_dao, item, True)
            finally:
                if locked:
                    lock_dao.unlock(item["id"])
