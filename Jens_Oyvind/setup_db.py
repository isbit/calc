import sqlite3
from sqlite3 import Error

database = "database.db"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

##### CREATE TABLES ######## 

sql_create_questionnaires_table = """CREATE TABLE IF NOT EXISTS questionnaires (
                                id_questionnaire INTEGER UNIQUE PRIMARY KEY NOT NULL,
                                name_questionnaire TEXT UNIQUE NOT NULL
                            );"""

sql_create_questionnaire_table = """CREATE TABLE IF NOT EXISTS questionnaire (
                                id_questionnaire INTEGER NOT NULL,
                                id_question INTEGER UNIQUE PRIMARY KEY NOT NULL,
                                question TEXT NOT NULL,
                                FOREIGN KEY (id_questionnaire) REFERENCES questionnaires(id_questionnaire)
                            );"""

sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id_user INTEGER UNIQUE PRIMARY KEY NOT NULL,
                                name TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL,
                                isadmin BOOLEAN NOT NULL,
                                profile_pic TEXT,
                                darkmode BOOLEAN,
                                tokens INT
                            );"""

sql_create_answers_table = """CREATE TABLE IF NOT EXISTS answers (
                                id_answer INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_questionnaire INTEGER NOT NULL,
                                id_question INTEGER NOT NULL, 
                                id_user INTEGER NOT NULL,
                                answer INTEGER NOT NULL,
                                FOREIGN KEY (id_question) REFERENCES questionnaire (id_question),
                                FOREIGN KEY (id_user) REFERENCES users (id_user)
                            );"""

sql_create_admin = """INSERT INTO users (id_user, name, password, isadmin, profile_pic, darkmode, tokens) 
                      VALUES (1, 'admin', 'scrypt:32768:8:1$EpoDsQL0nwLZwxqJ$48161cbcf91a61846674aa663934d965ffb664ed585c906282a0a4e7081e98fd3d9eb574ef3d7b0b6b25d29a17ca13b18cbfc70c3069ec6fecd483995c390302', 1, NULL, 0, 0);"""

sql_create_user = """INSERT INTO users (id_user, name, password, isadmin, profile_pic, darkmode, tokens) 
                     VALUES (2, 'user', 'scrypt:32768:8:1$KX1gJADWslGLNs2z$5328017b9a19b14af52c42fd4e16ba1c9111730ff2e6a00de9d174d060a180d3d53165d6a0b20d3098a9d9cbda5056499b4f0e16210586ff503d700c65103514', 0, 'static/uploads/user/user.jpg', 0, 0);"""

sql_create_user2 = """INSERT INTO users (id_user, name, password, isadmin, profile_pic, darkmode, tokens) 
                      VALUES (3, 'user2', 'scrypt:32768:8:1$KX1gJADWslGLNs2z$5328017b9a19b14af52c42fd4e16ba1c9111730ff2e6a00de9d174d060a180d3d53165d6a0b20d3098a9d9cbda5056499b4f0e16210586ff503d700c65103514', 0, 'static/uploads/user2/user2.jpg', 1, 0);"""

sql_create_user3 = """INSERT INTO users (id_user, name, password, isadmin, profile_pic, darkmode, tokens) 
                      VALUES (4, 'user3', 'scrypt:32768:8:1$KX1gJADWslGLNs2z$5328017b9a19b14af52c42fd4e16ba1c9111730ff2e6a00de9d174d060a180d3d53165d6a0b20d3098a9d9cbda5056499b4f0e16210586ff503d700c65103514', 0, NULL, 0, 0);"""

sql_create_user4 = """INSERT INTO users (id_user, name, password, isadmin, profile_pic, darkmode, tokens) 
                      VALUES (5, 'user4', 'scrypt:32768:8:1$KX1gJADWslGLNs2z$5328017b9a19b14af52c42fd4e16ba1c9111730ff2e6a00de9d174d060a180d3d53165d6a0b20d3098a9d9cbda5056499b4f0e16210586ff503d700c65103514', 0, NULL, 0, 0);"""


# Example data for questionnaires and questions
questionnaires = [
    (1, 'Worklife and stress'),
    (2, 'Health and wellness'),
    (3, 'Technology usage'),
    (4, 'Travel preferences'),
    (5, 'Food habits'),
    (6, 'Exercise routines'),
    (7, 'Reading habits'),
    (8, 'Music preferences'),
    (9, 'Movie preferences'),
    (10, 'Environmental awareness')
]

questions = [
    (1, 1, 'I work too much'),
    (1, 2, 'I like my colleagues'),
    (1, 3, 'I feel tired all the time'),
    (2, 4, 'I exercise regularly'),
    (2, 5, 'I eat healthy food'),
    (2, 6, 'I get enough sleep'),
    (3, 7, 'I use technology daily'),
    (3, 8, 'I prefer online shopping'),
    (3, 9, 'I am concerned about data privacy'),
    (4, 10, 'I love traveling'),
    (4, 11, 'I prefer solo travel'),
    (4, 12, 'I have a travel bucket list'),
    (5, 13, 'I enjoy cooking'),
    (5, 14, 'I prefer home-cooked meals'),
    (5, 15, 'I like trying new cuisines'),
    (6, 16, 'I exercise daily'),
    (6, 17, 'I prefer outdoor activities'),
    (6, 18, 'I have a gym membership'),
    (7, 19, 'I read books regularly'),
    (7, 20, 'I prefer fiction over non-fiction'),
    (7, 21, 'I have a favorite author'),
    (8, 22, 'I listen to music daily'),
    (8, 23, 'I prefer classical music'),
    (8, 24, 'I attend live concerts'),
    (9, 25, 'I watch movies regularly'),
    (9, 26, 'I prefer action movies'),
    (9, 27, 'I have a favorite director'),
    (10, 28, 'I am environmentally conscious'),
    (10, 29, 'I recycle regularly'),
    (10, 30, 'I support green initiatives')
]

answers = [
    # User 2 (4 questionnaires)
    (1, 1, 2, 1), (1, 2, 2, 5), (1, 3, 2, 5),
    (6, 16, 2, 1), (6, 17, 2, 1), (6, 18, 2, 2),
    (8, 22, 2, 1), (8, 23, 2, 3), (8, 24, 2, 5),
    (10, 28, 2, 5), (10, 29, 2, 1), (10, 30, 2, 1),

    # User 3 (5 questionnaires)
    (1, 1, 3, 3), (1, 2, 3, 4), (1, 3, 3, 2),
    (2, 4, 3, 5), (2, 5, 3, 4), (2, 6, 3, 3),
    (3, 7, 3, 2), (3, 8, 3, 3), (3, 9, 3, 4),
    (4, 10, 3, 5), (4, 11, 3, 4), (4, 12, 3, 3),
    (5, 13, 3, 2), (5, 14, 3, 3), (5, 15, 3, 4),

    # User 4 (4 questionnaires)
    (6, 16, 4, 5), (6, 17, 4, 4), (6, 18, 4, 3),
    (7, 19, 4, 2), (7, 20, 4, 3), (7, 21, 4, 4),
    (8, 22, 4, 5), (8, 23, 4, 4), (8, 24, 4, 3),
    (9, 25, 4, 2), (9, 26, 4, 3), (9, 27, 4, 4),

    # User 5 (3 questionnaires)
    (10, 28, 5, 5), (10, 29, 5, 4), (10, 30, 5, 3),
    (1, 1, 5, 2), (1, 2, 5, 3), (1, 3, 5, 4),
    (2, 4, 5, 5), (2, 5, 5, 4), (2, 6, 5, 3)
]


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#### INSERT #########

def insert_sql_statement(conn,sql):
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

def insert_many_sql_statement(conn, sql, data):
    try:
        c = conn.cursor()
        c.executemany(sql, data)
        conn.commit()
    except Error as e:
        print(e)

#### SETUP ####

def setup():
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_questionnaire_table)
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_questionnaires_table)
        create_table(conn, sql_create_answers_table)
        insert_sql_statement(conn, sql_create_admin)
        insert_sql_statement(conn, sql_create_user)
        insert_sql_statement(conn, sql_create_user2)
        insert_sql_statement(conn, sql_create_user3)
        insert_sql_statement(conn, sql_create_user4)
        insert_many_sql_statement(conn, "INSERT INTO questionnaires (id_questionnaire, name_questionnaire) VALUES (?, ?)", questionnaires)
        insert_many_sql_statement(conn, "INSERT INTO questionnaire (id_questionnaire, id_question, question) VALUES (?, ?, ?)", questions)
        insert_many_sql_statement(conn, "INSERT INTO answers (id_questionnaire, id_question, id_user, answer) VALUES (?, ?, ?, ?)", answers)

        conn.close()

if __name__ == '__main__':
    # If executed as main, this will create tables and insert initial data
    setup()

