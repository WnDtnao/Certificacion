import pymysql.cursors


class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="root",  # Cambia estos datos por los de tu MySQL
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)
                if query.lstrip().lower().startswith("insert"):
                    return cursor.lastrowid
                if cursor.description is not None:
                    return cursor.fetchall()
                return True
            finally:
                self.connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)
