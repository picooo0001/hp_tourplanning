from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ResourceClosedError
import logging
from datetime import *


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
        logging.basicConfig(filename='api_logs.log', level=logging.INFO)

    def get_session(self):
        """
        Erstellt eine Sitzung für Datenbankoperationen.

        Returns:
            Session: Eine Sitzung für Datenbankoperationen, wenn die Verbindung erfolgreich hergestellt wurde.
            str: Eine Nachricht über den Status der Verbindung. Wenn ein Fehler beim Verbindungsaufbau auftritt, wird eine entsprechende Fehlermeldung zurückgegeben.

        Raises:
            Exception: Wird ausgelöst, wenn ein Fehler beim Verbindungsaufbau auftritt.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            session = self.Session()
            message = "Verbindung erfolgreich hergestellt.", timestamp
            logging.info(message)  # Schreibe die Nachricht ins Logfile
            return session, message
        except Exception as e:
            message = f"Fehler beim Verbindungsaufbau: {str(e)}"
            logging.error(message)  # Schreibe die Fehlermeldung ins Logfile
            return None, message
        
class DatabaseDisconnector:
    """Verwaltet das Schließen der Datenbankverbindung."""
    def __init__(self, db_connector):
        """
        Initialisiert den Disconnector mit dem Connector.

        Args:
            db_connector (DatabaseConnector): Der DatabaseConnector für die Datenbankverbindung.
        """
        self.db_connector = db_connector
        logging.basicConfig(filename='api_logs.log', level=logging.INFO)

    def close_connection(self):
        """
        Schließt die Datenbankverbindung.

        Returns:
            bool: True, wenn die Verbindung erfolgreich geschlossen wurde oder bereits geschlossen ist, sonst False.
            str: Eine Nachricht über den Status des Verbindungsschlusses.

        Raises:
            Exception: Wird ausgelöst, wenn ein Fehler beim Schließen der Verbindung auftritt.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.db_connector.engine.dispose()
            message = "Verbindung erfolgreich geschlossen.", timestamp
            logging.info(message)  # Schreibe die Nachricht ins Logfile
            return True, message
        except ResourceClosedError:
            message = "Verbindung ist bereits geschlossen.", timestamp
            logging.warning(message)  # Schreibe die Warnung ins Logfile
            return True, message
        except Exception as e:
            message = f"Fehler beim Schließen der Verbindung: {str(e)}" , timestamp
            logging.error(message)  # Schreibe die Fehlermeldung ins Logfile
            raise Exception(message)


# Verbindung herstellen
db_connector = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
session, message = db_connector.get_session()

#Verbindung schließen
db_disconnector = DatabaseDisconnector(db_connector)
success, message = db_disconnector.close_connection()
