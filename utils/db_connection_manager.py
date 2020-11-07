from utils import read_ini_file
import os
import psycopg2


class ConnectionManager:
    """
    This class handles database connections
    __enter__() and __exit__() functions make this class acts like a context-manager
    Use it with "with ConnectionManager() as manager:" to not worry about closing connections and resource leaking
    """

    def __init__(self):
        self.con = None
        self.cur = None

    def __enter__(self):
        self.con, self.cur = self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    @staticmethod
    def connect():
        """ Connect to the db """
        conn = None
        cur = None
        try:
            # Get the config file path, root folder of the project
            config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.ini')

            # read connection parameters
            db_params = read_ini_file.read(filename=config_file, section="postgresql")

            # connect to the PostgreSQL server
            conn = psycopg2.connect(**db_params)

            # create a cursor
            cur = conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return conn, cur

    def close(self):
        """ This function closes db connection """

        # close the communication with the db
        self.cur.close()

        # close the connection
        if self.con is not None:
            self.con.close()
