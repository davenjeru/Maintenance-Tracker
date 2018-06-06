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
                             "id serial PRIMARY KEY," \
                             "email varchar UNIQUE NOT NULL," \
                             "password_hash varchar NOT NULL," \
                             "security_question varchar NOT NULL," \
                             "security_answer_hash varchar NOT NULL," \
                             "role varchar NOT NULL DEFAULT 'Consumer');"
        self.query(create_users_table)
        self.conn.commit()

        create_requests_table = "CREATE TABLE if not exists requests (" \
                                "id serial PRIMARY KEY," \
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

        create_token_blacklist_table = "CREATE TABLE if not exists tokens (" \
                                       "id serial PRIMARY KEY," \
                                       "jti varchar NOT NULL," \
                                       "expires timestamp NOT NULL);"
        self.query(create_token_blacklist_table)
        self.conn.commit()

    def drop_all(self):
        self.query("drop table requests;")
        self.query("drop table users;")
        self.query("drop table tokens;")
        self.conn.commit()

    def get_user_by_email(self, email: str):
        """
        Returns a dictionary with the user details if a user is found.
        Returns None otherwise
        :param email: the email to search with
        :rtype: dict
        """
        query = "select * from users where email={}".format("'" + email + "'")
        self.query(query)
        item = self.cur.fetchone()
        if not item:
            user = None
        else:
            user = dict(
                user_id=item[0],
                email=item[1],
                password_hash=item[2],
                security_question=item[3],
                security_answer_hash=item[4],
                role=item[5]
            )
        return user

    def save_user(self, user):
        email = user.email
        password_hash = user.password_hash
        security_question = user.security_question
        security_answer_hash = user.security_answer_hash
        role = user.role
        sql = 'insert into users(email, password_hash, security_question,' \
              ' security_answer_hash, role) values(%s, %s, %s, %s, %s)'
        data = (email, password_hash, security_question, security_answer_hash
                , role)
        self.cur = self.conn.cursor()
        self.cur.execute(sql, data)
        self.conn.commit()
