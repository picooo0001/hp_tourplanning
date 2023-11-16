from configparser import ConfigParser
import psycopg


class DatabaseConnector:
    """A class to establish and manage connections to a PostgreSQL database."""

    def __init__(self, filename="db.ini", section="postgresql"):
        """
        Initialize the DatabaseConnector.

        Args:
        - filename (str): The name of the configuration file.
        - section (str): The section in the configuration file containing
                         PostgreSQL connection parameters.
        """
        self.filename = filename
        self.section = section

    def read_config(self):
        """
        Read the configuration file and extract PostgreSQL connection parameters.

        Returns:
        - dict: A dictionary containing PostgreSQL connection parameters.
        """
        parser = ConfigParser()
        parser.read(self.filename)

        database = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                database[param[0]] = param[1]
        else:
            raise Exception(
                f"Section {self.section} not found in the {self.filename} file"
            )
        return database

    def connect(self):
        """
        Establish a connection to the PostgreSQL database using configuration parameters.

        Prints the database version and closes the connection.
        """
        connection = None
        try:
            params = self.read_config()

            print("Connecting to the PostgreSQL database...")
            connection = psycopg.connect(**params)
            var_cur = connection.cursor()

            print("Database version is:")
            var_cur.execute("SELECT version()")
            version_of_database = var_cur.fetchone()
            print(version_of_database)

            var_cur.close()
        except (Exception, psycopg.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print("Database connection closed")


if __name__ == "__main__":
    db_connector = DatabaseConnector()
    db_connector.connect()
