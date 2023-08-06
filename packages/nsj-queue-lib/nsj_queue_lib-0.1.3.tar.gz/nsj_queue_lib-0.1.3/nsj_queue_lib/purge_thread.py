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
    QUEUE_MINUTE_PURGE_THREAD,
    QUEUE_PURGE_MAX_AGE,
    QUEUE_PURGE_LIMIT,
    QUEUE_TABLE,
    GLOBAL_RUN,
    logger,
)


class PurgeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        Roda um loop de exclusão das tarefas muito antigas

        A thread só roda de fato nos minutos configurados na
        variável de ambiente: QUEUE_MINUTE_PURGE_THREAD (com
        valor padrão: 0).

        Além disso, é pego um lock no BD, para que apenas um
        worker realize essa operação por vez (para não
        sobrecarregar o banco).
        """

        logger.info("Thread de purge iniciada.")
        while GLOBAL_RUN:
            # Aguardando 15 segundos a cada verificação se deve rodar
            time.sleep(15)
            logger.debug("Nova verificação da thread de purge")

            # Recuperando o minuto atual
            now = datetime.now()
            if not (str(now.minute) in QUEUE_MINUTE_PURGE_THREAD.split(",")):
                continue

            logger.debug("Vai iniciar, de fato, a thread de purge")

            try:
                with DBConnectionPsycopg2(
                    DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                ) as dbconn:
                    db = DBAdapter3(dbconn.conn)
                    lock_dao = LockDAO(db)

                    lock = False
                    try:
                        if lock_dao.try_lock_purge():
                            lock = True
                        else:
                            logger.debug(
                                "Desistindo do purge, porque já há outro worker operando o mesmo."
                            )
                            continue

                        logger.info("Iniciando tratamento de purge...")

                        dao = TarefaDAO(db, QUEUE_TABLE)
                        self._purge(dao)

                    finally:
                        if lock:
                            lock_dao.unlock_purge()

            except Exception as e:
                logger.exception(f"Erro desconhecido: {e}", e, stack_info=True)
                logger.info(
                    "Aguardando 5 segundos, para tentar nova conexão com o banco de dados."
                )
                time.sleep(5)

        logger.info("Thread de purge finalizada.")

    def _purge(self, dao: TarefaDAO):
        """
        Apaga as tarefas antigas, de acordo com a configuração
        (QUEUE_PURGE_MAX_AGE).
        """

        deleted = 1
        count = 1
        while deleted > 1 and count <= 100:
            _, deleted = dao.purge(QUEUE_PURGE_MAX_AGE, QUEUE_PURGE_LIMIT)
            logger.info(
                f"Purge executado. Registros excluídos: {deleted}. Rodada de purge: {count}"
            )

            count += 1
