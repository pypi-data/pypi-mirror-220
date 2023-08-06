import time

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3
from nsj_sql_utils_lib.dbconection_psycopg2 import DBConnectionPsycopg2

from nsj_queue_lib.settings import (
    DB_HOST,
    DB_PORT,
    DB_BASE,
    DB_USER,
    DB_PASS,
)


def _load_scene(db: DBAdapter3):
    sql = """
        insert into fila_teste (origem, destino, processo, chave_externa, payload) values
        ('dbeaver', 'codigo', 'teste_da_fila', '123456', 'conteudo da mensagem, pode ser muito complexo')
        returning id
    """
    resp, _ = db.execute(sql)

    return resp[0]["id"]


def _get_tarefa(db: DBAdapter3, tarefa_id: int):
    sql = """
        select * from fila_teste where id=%(id)s
    """
    resp, _ = db.execute(sql, id=tarefa_id)

    return resp[0]


def _delete_tarefa(db: DBAdapter3, tarefa_id: int):
    sql = """
        delete from fila_teste where id=%(id)s
    """
    _, count = db.execute(sql, id=tarefa_id)

    return count


def test_push_notification():
    with DBConnectionPsycopg2(DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS) as dbconn:
        db = DBAdapter3(dbconn.conn)

        tarefa_id = _load_scene(db)

        time.sleep(5)

        tarefa = _get_tarefa(db, tarefa_id)

        assert tarefa["status"] == "sucesso"

        count = _delete_tarefa(db, tarefa_id)

        assert count == 1
