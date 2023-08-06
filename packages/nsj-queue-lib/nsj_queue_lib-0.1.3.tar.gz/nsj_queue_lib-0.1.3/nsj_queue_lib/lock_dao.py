from nsj_sql_utils_lib.dbadapter3 import DBAdapter3


class LockDAO:
    LOCK_ID_RETRY = 1
    LOCK_ID_PURGE = 2
    LOCK_ID_NOTIFY = 3

    SQL_LOCK = """
    SELECT pg_try_advisory_lock(%(value)s) as lock
    """

    SQL_UNLOCK = """
    SELECT pg_advisory_unlock(%(value)s)
    """

    def __init__(self, db: DBAdapter3):
        self._db = db

    def try_lock_retry(self) -> bool:
        return self.try_lock(LockDAO.LOCK_ID_RETRY)

    def unlock_retry(self):
        self.unlock(LockDAO.LOCK_ID_RETRY)

    def try_lock_purge(self) -> bool:
        return self.try_lock(LockDAO.LOCK_ID_PURGE)

    def unlock_purge(self):
        self.unlock(LockDAO.LOCK_ID_PURGE)

    def try_lock_notify(self) -> bool:
        return self.try_lock(LockDAO.LOCK_ID_NOTIFY)

    def unlock_notify(self):
        self.unlock(LockDAO.LOCK_ID_NOTIFY)

    def try_lock(self, value: int) -> bool:
        result, _ = self._db.execute(LockDAO.SQL_LOCK, value=value)
        return result[0]["lock"] or False

    def unlock(self, value: int):
        self._db.execute(LockDAO.SQL_UNLOCK, value=value)
