import os

import psycopg2


class Database:
    def __init__(self,
                 db: str = os.getenv('DB_NAME'),
                 user: str = os.getenv('DB_USER'),
                 password: str = os.getenv('DB_PASSWORD'),
                 host: str = os.getenv('DB_HOST'),
                 port: int = os.getenv('DB_PORT')
                 ):

        self.conn = psycopg2.connect(database=db,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=int(port))
        self.cur = None

    def query(self, query):
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(query)
        except Exception as e:
            self.cur.connection.rollback()
            return e.args[0]

    def close(self):
        self.cur.close()
        self.conn.close()

    def create_all(self):
        create_users_table = "CREATE TABLE if not exists users (" \
                             "id integer PRIMARY KEY," \
                             "email varchar UNIQUE NOT NULL," \
                             "password_hash varchar NOT NULL," \
                             "security_question varchar NOT NULL," \
                             "security_answer_hash varchar NOT NULL);"
        self.query(create_users_table)
        self.conn.commit()

        create_requests_table = "CREATE TABLE if not exists requests (" \
                                "id integer PRIMARY KEY," \
                                "user_id integer references" \
                                " users(id) NOT NULL," \
                                "title varchar NOT NULL," \
                                "description varchar NOT NULL," \
                                "status varchar NOT NULL" \
                                " DEFAULT 'Pending Approval'," \
                                "date_requested date NOT NULL," \
                                "last_modified date," \
                                "requested_by varchar not null);"
        self.query(create_requests_table)
        self.conn.commit()
