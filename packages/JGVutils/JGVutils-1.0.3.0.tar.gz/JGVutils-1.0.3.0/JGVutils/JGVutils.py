import sqlite3  # Import the SQLite3 module for database access.
import json  # Import the JSON module for working with JSON data.
import os  # Import the OS module for working with files and directories.
import mysql.connector  # Import the MySQL Connector module for working with MySQL databases.

class Utils:
    @staticmethod
    def input(message="", type=str, default=None, error_message=None):
        """
        A static method that prompts the user for input, converts the input to the specified data type, and returns the input.
        
        Args:
        message (str): The message to display to the user when prompting for input.
        type (type): The data type to convert the input to. Defaults to str.
        default: The default value to return if an exception occurs during input or conversion. Defaults to None.
        error_message (str): The error message to display if an exception occurs during input or conversion. 
            Defaults to None, which means no error message will be displayed.
        
        Returns:
        The user's input, converted to the specified data type, or the default value if an exception occurred.
        """
        try:
            return type(input(message))
        except:
            if error_message is not None:
                print(error_message)
        return default

    @staticmethod
    def return_json(array, format=True, indent=4, sort_keys=False):
        """
        A static method that returns a JSON representation of a Python object.
        
        Args:
        array: The Python object to convert to a JSON string.
        format (bool): A boolean indicating whether to format the JSON output with indentation and line breaks. 
            Defaults to True.
        indent (int): The number of spaces to use for indentation when formatting the JSON output. 
            Only used if format=True. Defaults to 4.
        sort_keys (bool): A boolean indicating whether to sort the keys of the JSON output alphabetically. 
            Defaults to False.
        
        Returns:
        A JSON string representing the input Python object.
        """
        if format:
            return json.dumps(array, indent=indent, sort_keys=sort_keys)
        return json.dumps(array, separators=(",", ":"), sort_keys=sort_keys)

class SQLiteConnection:
    """
    This class represents a connection to a SQLite database. It provides methods to load SQL commands from a file,
    execute SQL queries, and check if a database connection has been established.

    Attributes:
        path (str): A string representing the path to the SQLite database file.

    Methods:
        is_database_connection(): Returns True if the database file exists in the specified path, else False.
        load_commands(path_file: str) -> str: Loads and executes SQL commands from the provided file path in the SQLite
            database. Returns 'Correct' on successful execution, else 'Error'.
        execute_query(query: str, args: list = [], type_fetch: str = 'dict', commit: bool = False) -> list or dict:
            Executes the provided SQL query with optional parameters and returns the result set in a list of dictionaries
            or list of tuples, based on the `type_fetch` parameter. If `commit` is True, the transaction will be
            committed. Returns None if an error occurs during execution.
    """
    def __init__(self, path):
        """
        Initializes the SQLiteConnection object.

        Args:
            path (str): The path to the SQLite database file.
        """
        self.path = path

    def is_database_connection(self):
        """
        Checks if the SQLite database connection exists.

        Returns:
            bool: True if the connection exists, False otherwise.
        """
        return os.path.isfile(self.path)
    
    def load_commands(self, path_file):
        """
        Executes SQL commands from a file on the SQLite database.

        Args:
            path_file (str): The path to the file containing SQL commands.

        Returns:
            str: "Correct" if the execution was successful, "Error" otherwise.
        """
        if self.is_database_connection():
            # Connects to the database
            connection = sqlite3.connect(self.path)
            # Creates a cursor object
            cursor = connection.cursor()
            # Reads the commands from the SQL script file
            with open(path_file, "r") as f:
                comandos = f.read()
            # Executes the commands in the SQL script file
            cursor.executescript(comandos)
            # Commits the changes to the database
            connection.commit()
            # Closes the database connection
            connection.close()
            return "Correct"
        # Returns an error message if the database connection is invalid
        return "Error"

    def execute_query(self, query, args=[], type_fetch="dict", commit=False):
        """
        Executes a SQL query on the SQLite database.

        Args:
            query (str): The SQL query to execute.
            args (list): The list of arguments to pass to the query.
            type_fetch (str): The type of fetch result to return. Options are "dict" or "list".
            commit (bool): If True, commits the changes to the database.

        Returns:
            list: A list of dictionaries or tuples representing the result of the query.
        """
        try:
            # Connects to the database
            connection = sqlite3.connect(self.path)
            # Checks whether the database connection is valid
            if self.is_database_connection():
                # If type_fetch is set to "dict", returns the results as a list of dictionaries
                if type_fetch == "dict":
                    connection.row_factory = sqlite3.Row
                # Creates a cursor object
                cursor = connection.cursor()
                # Returns the results as a list of dictionaries
                connection.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
                # Executes the SQL query with the specified arguments
                cursor.execute(query, args)
                # Commits the changes to the database if commit is set to True
                if commit:
                    connection.commit()
                # Fetches all the rows returned by the SQL query
                rows = cursor.fetchall()
                # Closes the cursor object
                cursor.close()

                # If type_fetch is set to "dict", returns the results as a list of dictionaries
                if type_fetch == "dict":
                    return [dict(row) for row in rows]
                # Otherwise, returns the results as a list of tuples
                return rows
        # Returns None if an error occurs while executing the SQL query
        except:
            pass
        return None


class MySQLConnection:
    """
    Class that represents a connection to a MySQL database.

    Attributes:
    - host (str): IP address or hostname where the database is located. Defaults to "localhost".
    - port (int): port number where the database is located. Defaults to 3306.
    - dbname (str): name of the database to connect to.
    - username (str): username to authenticate with the database.
    - password (str): password to authenticate with the database.

    Methods:
    - is_database_connection(): Checks if a connection to the specified database can be established.
    - execute_query(query, args=[], type_fetch="dict", commit=False): Executes an SQL query on the specified database.
        - query (str): SQL query to execute.
        - args (list): list of arguments for the SQL query. Defaults to an empty list.
        - type_fetch (str): type of data to retrieve from the query. Can be "dict" (dictionary) or "tuple". Defaults to "dict".
        - commit (bool): if True, commits the transaction after executing the query. Defaults to False.

    """
    def __init__(self, host="localhost", port=3306, dbname="dbname", username="root", password=""):
        """
        Constructor for the MySQLConnection class.

        Parameters:
        - host (str): IP address or hostname where the database is located. Defaults to "localhost".
        - port (int): port number where the database is located. Defaults to 3306.
        - dbname (str): name of the database to connect to.
        - username (str): username to authenticate with the database.
        - password (str): password to authenticate with the database.

        """
        self.host = host
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password

    def is_database_connection(self):
        """
        Checks if a connection to the specified database can be established.

        Returns:
        - True if a connection can be established, False otherwise.

        """
        try:
            # Establishes a connection to the database using the specified credentials
            mysql.connector.connect(host=self.host, port=self.port, user=self.username, passwd=self.password, database=self.dbname)
            return True
        except:
            pass
        # Return False on error
        return False

    def execute_query(self, query, args=[], type_fetch="dict", commit=False):
        """
        Executes an SQL query on the specified database.

        Parameters:
        - query (str): SQL query to execute.
        - args (list): list of arguments for the SQL query. Defaults to an empty list.
        - type_fetch (str): type of data to retrieve from the query. Can be "dict" (dictionary) or "tuple". Defaults to "dict".
        - commit (bool): if True, commits the transaction after executing the query. Defaults to False.

        Returns:
        - If type_fetch is "dict", returns a list of dictionaries representing the query results.
        - If type_fetch is "tuple", returns a list of tuples representing the query results.

        """
        try:
            # Establishes a connection to the database using the specified credentials
            connection = mysql.connector.connect(host=self.host, port=self.port, user=self.username, passwd=self.password, database=self.dbname)
            # Creates a cursor object to execute the SQL query on the database
            cursor = connection.cursor(dictionary = type_fetch == "dict")
            # Executes the SQL query using the cursor object
            cursor.execute(query)
            # Retrieves all rows of the query result
            rows = cursor.fetchall()
            # Closes the cursor and connection to the database
            cursor.close()
            connection.close()
            # If the desired fetch type is not a dictionary, converts the result to a list of tuples
            if type_fetch != "dict":
                rows = [row[0] if len(row) == 1 else row for row in rows]  
            # Returns the result of the query
            return rows
        except:
            # If an error occurs, returns None
            pass
        return None