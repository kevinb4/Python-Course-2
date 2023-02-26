import pymysql

class DB_Connect():
    """A simple class for connecting to a database and performing queries"""

    def __init__(self, passed_db_username, passed_db_password, passed_database):
        """Initialize name and age variables/attributes"""
        self.passed_db_username = passed_db_username
        self.passed_db_password = passed_db_password
        self.passed_database = passed_database
        self.conn = None

    def __connect(self):
        """Creates connections to the database when they are needed"""
        self.conn = pymysql.connect(host='localhost',
                        user=self.passed_db_username,
                        password=self.passed_db_password,
                        db=self.passed_database,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

    def executeQuery(self, passed_query, passed_args = None):
        """Executes a database query for Inserts, Updates, and Deletes"""

        if not self.conn:
            self.__connect()

        with self.conn.cursor() as cursor:
            if passed_args:
                cursor.execute(passed_query, passed_args)
            else:
                cursor.execute(passed_query)

    def executeSelectQuery(self, passed_query, passed_args = None):
        """Executes a SELECT database query and returns the results as a tuple-like structure"""

        if not self.conn:
            self.__connect()

        with self.conn.cursor() as cursor:
            if passed_args:
                cursor.execute(passed_query, passed_args)
            else:
                cursor.execute(passed_query)

        return cursor.fetchall()

    def close_connection(self):
        """Closes the database connection"""

        self.conn.close()
