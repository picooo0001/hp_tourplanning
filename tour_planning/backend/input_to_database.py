from db_connect_disconnect import DatabaseConnector
from orm import Tour, Address, Client
from user_input import TourCreation
from background_checks import BackgroundChecks
from log_config import LogConfig
from sqlalchemy import and_

class DataWriter:
    """Klasse zum Schreiben von Daten in die Datenbank.

    Verantwortlich für die Erstellung von Einträgen für Touren, Adressen und Kunden in der Datenbank.

    Attributes:
        db_connector (DatabaseConnector): Eine Instanz der DatabaseConnector-Klasse für die Datenbankverbindung.
        session: Die aktuelle Datenbanksitzung.
        tourcreation (TourCreation): Eine Instanz der TourCreation-Klasse für die Eingabe von Tourdaten.
        logger: Der Logger für das Schreiben von Logmeldungen.
    """

    def __init__(self):
        """Initialisiert die DataWriter-Klasse."""
        self.db_connector = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
        self.session, _ = self.db_connector.get_session()
        self.tourcreation = TourCreation()
        log_config = LogConfig()
        self.logger = log_config.setup_logger('db_entry_log', 'db_entry.log')

    def create_db_entry(self):
        """Erstellt neue Einträge für Tour, Adresse und Kunde."""
        self.new_tour = Tour(date=self.tourcreation.date_input(), 
                        kolonne_type=self.tourcreation.kolonne_input(),
                        private=self.tourcreation.input_private(),
                        further_info=self.tourcreation.input_info())
        
        self.new_address = Address(strasse=self.tourcreation.input_strasse(),
                              hausnr=self.tourcreation.input_hausnr(),
                              plz=self.tourcreation.input_plz(),
                              ort=self.tourcreation.input_ort())
        
        existing_address = self.session.query(Address).filter(
             and_(
                  Address.strasse == self.new_address.strasse,
                  Address.hausnr == self.new_address.hausnr,
                  Address.plz == self.new_address.plz,
                  Address.ort == self.new_address.ort
             )
        ).first()

        if existing_address:
             self.new_address = existing_address
        else:
             self.new_address = self.new_address

        self.new_client = Client(firmenname=self.tourcreation.input_firmenname())

    def check_address(self):
        """Überprüft die Existenz einer Adresse und speichert sie in der Datenbank, falls gewünscht."""
        validator = BackgroundChecks(strasse=self.new_address.strasse,
                                     hausnr=self.new_address.hausnr,
                                     plz=self.new_address.plz,
                                     ort=self.new_address.ort)
        if validator.check_adress_existance():
            if self.tourcreation.ask_user_to_save_input():
                print("Adresse wird in datenbank gespeichert")
                return True
            else:
                print("Speicherung abgebrochen")
                return False
        else:
            print("Diese Adresse existiert nicht")
            return False
    
    def write_tour_data_to_db(self):
        """Schreibt Tourdaten in die Datenbank und ordnet sie Adressen und Kunden zu."""
        try:
            self.create_db_entry()
            if self.check_address():
                self.session.add(self.new_client)
                self.session.add(self.new_address)
                self.session.commit()

                client_id = self.new_client.client_id
                address_id = self.new_address.address_id

                self.new_tour.client_id = client_id
                self.new_tour.address_id = address_id

                self.session.add(self.new_tour)
                self.session.commit()
                self.logger.info("Datenbankeintrag erfolgreich erstellt und Adressen/Touren/Clients zugeordnet.")
            else:
                pass
        except Exception as e:
                log_message = f"Fehler beim Erstellen des Datenbankeintrags: {str(e)}"
                self.logger.error(log_message)

                self.session.rollback()
                self.logger.warning("Rollback erfolgreich durchgeführt.")
                raise  
        finally:
                self.db_connector.close_connection()
                self.logger.info("Datenbankverbindung geschlossen.")
 
if __name__ == "__main__":
    db_connector = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
    establish_connection = db_connector.get_session()

    db_writer = DataWriter()
    db_writer.write_tour_data_to_db()









