import sqlite3

from django.db import transaction

from tools.gestor_importers.clients_importer import ClientsImporter
from tools.gestor_importers.trailers_importer import TrailerImporter


class QueryCtl:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def load_sql_file(self, file_path: str):
        with open(file_path, "r") as file:
            sql = file.read()
        return sql

    def exec_query(self, file: str) -> list[tuple]:
        sql = self.load_sql_file(file)
        self.cursor.execute(sql)
        return self.cursor.fetchall()


@transaction.atomic
def import_data():
    qc = QueryCtl("db.sqlite3")

    ti = TrailerImporter()
    rows = qc.exec_query(f"tools/gestor_importers/{ti.sql_file}")
    ti.save(rows)

    ci = ClientsImporter()
    rows = qc.exec_query(f"tools/gestor_importers/{ci.sql_file}")
    ci.save(rows)


import_data()
