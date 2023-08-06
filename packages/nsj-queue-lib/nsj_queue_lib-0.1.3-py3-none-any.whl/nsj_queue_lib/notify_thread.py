import threading
import time

from datetime import datetime

from nsj_sql_utils_lib.dbconection_psycopg2 import DBConnectionPsycopg2
from nsj_sql_utils_lib.dbadapter3 import DBAdapter3

from nsj_queue_lib.lock_dao import LockDAO
from nsj_queue_lib.tarefa_dao import TarefaDAO
from nsj_queue_lib.settings import (
    DB_HOST,
    DB_PORT,
    DB_BASE,
    DB_USER,
    DB_PASS,
    QUEUE_NAME,
    QUEUE_MINUTE_NOTIFY_THREAD,
    QUEUE_TABLE,
    GLOBAL_RUN,
    logger,
)


class NotifyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        Roda um loop de disparo de notificações para tarefas
        agendadas (e que já possam ser executadas).

        A thread só roda de fato nos minutos configurados na
        variável de ambiente: QUEUE_MINUTE_NOTIFY_THREAD (com
        valor padrão: 0,5,10,15,20,25,30,35,40,45,50,55).

        Além disso, é pego um lock no BD, para que apenas um
        worker realize essa operação por vez (para não
        sobrecarregar o banco).
        """

        logger.info("Thread de notify iniciada.")
        while GLOBAL_RUN:
            # Aguardando 15 segundos a cada verificação se deve rodar
            time.sleep(15)
            logger.debug("Nova verificação da thread de notify")

            # Recuperando o minuto atual
            now = datetime.now()
            if not (str(now.minute) in QUEUE_MINUTE_NOTIFY_THREAD.split(",")):
                continue

            logger.debug("Vai iniciar, de fato, a thread de notify")

            try:
                with DBConnectionPsycopg2(
                    DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                ) as dbconn:
                    db = DBAdapter3(dbconn.conn)
                    lock_dao = LockDAO(db)

                    lock = False
                    try:
                        if lock_dao.try_lock_notify():
                            lock = True
                        else:
                            logger.debug(
                                "Desistindo do notify, porque já há outro worker operando o mesmo."
                            )
                            continue

                        logger.info("Iniciando tratamento de notify...")

                        dao = TarefaDAO(db, QUEUE_TABLE)
                        self._notify(dao)

                    finally:
                        if lock:
                            lock_dao.unlock_notify()

            except Exception as e:
                logger.exception(f"Erro desconhecido: {e}", e, stack_info=True)
                logger.info(
                    "Aguardando 5 segundos, para tentar nova conexão com o banco de dados."
                )
                time.sleep(5)

        logger.info("Thread de purge finalizada.")

    def _notify(self, dao: TarefaDAO):
        """
        Recupera as tarefas agendadas que precisam de notify,
        marcando-as como pendentes, disparando o notify para elas.
        """

        agendadas, count = dao.list_agendadas_para_notificacao()
        logger.info(
            f"Verificando tarefas agendadas e pendentes de notificação para execução. Quantidade recuperada: {count}"
        )

        for tarefa in agendadas:
            try:
                logger.debug(
                    f"Atualizando tarefa de agendada para pendente. ID: {tarefa['id']}"
                )

                # Abrindo transação
                dao.db.begin()

                # Atualizando status da tarefa para pendente
                dao.update_status(tarefa["id"], "pendente")

                # Notificando a fila (para acordar os workers)
                dao.notify(QUEUE_NAME)

                # Commitando transação
                dao.db.commit()
            finally:
                # Fazendo rollback (se houver commit anterior, não faz nada)
                dao.db.rollback()
