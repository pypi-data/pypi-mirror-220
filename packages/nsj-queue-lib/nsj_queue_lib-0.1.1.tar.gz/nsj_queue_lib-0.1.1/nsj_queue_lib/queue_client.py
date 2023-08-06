import datetime

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3

from tarefa_dao import TarefaDAO


class QueueClient:
    def __init__(self, bd_conn) -> None:
        self._tarefa_dao = TarefaDAO(DBAdapter3(bd_conn))

    def insert_task(
        self,
        origem: str,
        destino: str,
        processo: str,
        chave_externa: str,
        payload: str,
        tenant: int = None,
        grupo_empresarial: str = None,
        data_hora: datetime.datetime = None,
    ):
        # Criando o objeto para realizar o insert
        task = {
            "origem": origem,
            "destino": destino,
            "processo": processo,
            "chave_externa": chave_externa,
            "payload": payload,
        }

        if tenant is not None:
            task["tenant"] = tenant

        if grupo_empresarial is not None:
            task["grupo_empresarial"] = grupo_empresarial

        if data_hora is not None:
            task["data_hora"] = data_hora
            task["data_hora_inicial"] = data_hora

        # Inserinfo a tarefa
        self._tarefa_dao.insert(task)


# CODIGO DE TESTE MANUAL ABAIXO
# from nsj_queue_lib.settings import (
#     DB_HOST,
#     DB_PORT,
#     DB_BASE,
#     DB_USER,
#     DB_PASS,
# )

# from nsj_sql_utils_lib.dbconection_psycopg2 import DBConnectionPsycopg2

# with DBConnectionPsycopg2(DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS) as dbconn:
#     queue_client = QueueClient(dbconn.conn)
#     queue_client.insert_task(
#         "teste",
#         "teste_destino",
#         "processo_teste",
#         "1234567",
#         "conteúdo da mensagem",
#         1,
#         "grupo",
#     )
