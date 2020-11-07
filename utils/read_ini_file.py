from configparser import ConfigParser
import os


def read(filename, section):
    """ This function read database.ini file and returns connection parameters as dictionary. """

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    params_dict = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            params_dict[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return params_dict


def get_connection_string():
    """ Generates connection string """

    # Get the config file path, root folder of the project
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.ini')

    # read connection parameters
    params = read(filename=config_file, section="postgresql")

    # 'postgresql://user:password@host:port/database'
    connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(params["user"],
                                                             params["password"],
                                                             params["host"],
                                                             params["port"],
                                                             params["database"])
    return connection_string
