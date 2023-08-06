import time

from nsj_queue_lib.dbadapter import DBAdapter
from nsj_queue_lib.dbconection import DBConnection
from nsj_queue_lib.settings import (
    DB_HOST,
    DB_PORT,
    DB_BASE,
    DB_USER,
    DB_PASS,
)


def _load_scene(db: DBAdapter):
    sql = """
        insert into fila_teste (origem, destino, processo, chave_externa, payload) values
        ('dbeaver', 'codigo', 'teste_da_fila', '123456', 'conteudo da mensagem, pode ser muito complexo')
        returning id
    """
    resp, _ = db.execute(sql)

    return resp[0]["id"]


def _get_tarefa(db: DBAdapter, tarefa_id: int):
    sql = """
        select * from fila_teste where id=%(id)s
    """
    resp, _ = db.execute(sql, id=tarefa_id)

    return resp[0]


def _delete_tarefa(db: DBAdapter, tarefa_id: int):
    sql = """
        delete from fila_teste where id=%(id)s
    """
    _, count = db.execute(sql, id=tarefa_id)

    return count


def test_push_notification():
    with DBConnection(DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS) as dbconn:
        db = DBAdapter(dbconn.conn)

        tarefa_id = _load_scene(db)

        time.sleep(5)

        tarefa = _get_tarefa(db, tarefa_id)

        assert tarefa["status"] == "sucesso"

        count = _delete_tarefa(db, tarefa_id)

        assert count == 1
