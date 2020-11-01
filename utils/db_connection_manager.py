from configparser import ConfigParser
import os
import psycopg2


class ConnectionManager:

    def __init__(self):
        pass

    def connect(self):
        """ Connect to the db """
        conn = None
        cur = None
        try:
            # Get the config file path, root folder of the project
            config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.ini')

            # read connection parameters
            db_params = self.get_config(filename=config_file)

            # connect to the PostgreSQL server
            conn = psycopg2.connect(**db_params)

            # create a cursor
            cur = conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return conn, cur

    @staticmethod
    def close(connection, cursor):
        """ This function closes db connection """

        # close the communication with the db
        cursor.close()

        # close the connection
        if connection is not None:
            connection.close()

    @staticmethod
    def get_config(filename="database.ini", section='postgresql'):
        """ This function read database.ini file and returns connection parameters as dictionary. """

        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db_params = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db_params[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db_params

    def get_connection_string(self):
        """ Generates connection string """

        # Get the config file path, root folder of the project
        config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.ini')

        # read connection parameters
        params = self.get_config(filename=config_file)
        connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(params["user"],
                                                                 params["password"],
                                                                 params["host"],
                                                                 params["port"],
                                                                 params["database"])
        # 'postgresql://scott:tiger@localhost:5432/mydatabase'
        return connection_string
