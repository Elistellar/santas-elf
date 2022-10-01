from sqlite3 import connect
from typing import Any

from .file_manager import path
from .log import log


class Database:
    
    tables = {
        "users": {
            "user_id": int,
        },
        "pairs": {
            "from_id": int,
            "to_id": int,
        }
    }
    
    types = {
        int: "INT",
        bool: "BOOLEAN",
        str: "TEXT"
    }
    
    @classmethod
    def init(cls):
        cls.con = connect(path("database.db"))
        cls.cur = cls.con.cursor()
        
        # create tables if not exists
        for name, data in cls.tables.items():
            cls.cur.execute(f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join([f'{key} {cls.types[val]}' for key, val in data.items()])})")
            data.update({"id": int})

        cls.con.commit()
        
    @classmethod
    def insert(cls, table: str, values: dict[str, Any]):
        
        sql = f"INSERT INTO {table} ({', '.join(values.keys())}) VALUES ({', '.join([str(val) if isinstance(val, int) else '`' + val + '`' for val in values.values() ])})".replace("None", "NULL").replace("`", "'")
        log.sql(sql)
        
        cls.cur.execute(sql)
        cls.con.commit()
        
    @classmethod
    def select(cls, table: str, vars: list[str] = ["*"], where: str = None, order: str = None) -> list[dict[str, Any]]:
        sql = f"SELECT {', '.join(vars)} FROM {table}{' WHERE ' + where if where else ''}{' ORDER BY ' + order if order else ''}"
        log.sql(sql)
        cls.cur.execute(sql)
        
        if vars == ["*"]:
            vars = ["id"] + list(cls.tables[table].keys())
            del vars[-1]

        r = [
            {
                var: cls.tables[table][var](val) if val not in [None, 'None'] else None
                for var, val in zip(vars, row)
            }
            for row in cls.cur.fetchall()
        ]
        
        lenr = len(r)
        log.sql(f"-> {lenr} result{'s' if lenr > 1 else ''}" + str(":\n                 - " if lenr > 0 else "") + "\n                 - ".join([str(row) for row in r]))
        return r

    @classmethod
    def delete(cls, table: str, where: str = None):
        sql = f"DELETE FROM {table}{' WHERE ' + where if where else ''}"
        log.sql(sql)
        cls.cur.execute(sql)
        cls.con.commit()

    @classmethod
    def update(cls, table: str, values: dict[str, Any], where: str):
        sql = f"UPDATE {table} SET {', '.join([var + '=`' + str(val) + '`' for var, val in values.items()])}{' WHERE ' + where if where else ''}".replace("`", "'")
        log.sql(sql)
        cls.cur.execute(sql)
        cls.con.commit()
