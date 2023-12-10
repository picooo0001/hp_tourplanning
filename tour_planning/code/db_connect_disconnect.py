from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ResourceClosedError
from log_config import LogConfig

class DatabaseConnector:
    """Stellt eine Verbindung zur Datenbank her und verwaltet Sitzungen für Datenbankoperationen."""
    def __init__(self, db_url):
        """
        Initialisiert eine neue Datenbankverbindung.

        Args:
            db_url (str): Die URL zur Datenbank.
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        log_config = LogConfig()
        self.logger = log_config.setup_logger('db_connection_logger', 'db_connection.log')

    def get_session(self):
        """
        Erstellt eine Sitzung für Datenbankoperationen.

        Returns:
            Session: Eine Sitzung für Datenbankoperationen, wenn die Verbindung erfolgreich hergestellt wurde.
            str: Eine Nachricht über den Status der Verbindung. Wenn ein Fehler beim Verbindungsaufbau auftritt, wird eine entsprechende Fehlermeldung zurückgegeben.

        Raises:
            Exception: Wird ausgelöst, wenn ein Fehler beim Verbindungsaufbau auftritt.
        """
        try:
            session = self.Session()
            message = "Verbindung erfolgreich hergestellt."
            self.logger.info(message)
            return session, message
        except Exception as e:
            message = f"Fehler beim Verbindungsaufbau: {str(e)}"
            self.logger.error(message)
            return None, message
        
    def close_connection(self):
        """
        Schließt die Datenbankverbindung.

        Returns:
            bool: True, wenn die Verbindung erfolgreich geschlossen wurde oder bereits geschlossen ist, sonst False.
            str: Eine Nachricht über den Status des Verbindungsschlusses.

        Raises:
            Exception: Wird ausgelöst, wenn ein Fehler beim Schließen der Verbindung auftritt.
        """
        try:
            self.engine.dispose()
            message = "Verbindung erfolgreich geschlossen."
            self.logger.info(message)
            return True, message
        except ResourceClosedError:
            message = "Verbindung ist bereits geschlossen."
            self.logger.warning(message)
            return True, message
        except Exception as e:
            message = f"Fehler beim Schließen der Verbindung: {str(e)}"
            self.logger.error(message)
            raise Exception(message)