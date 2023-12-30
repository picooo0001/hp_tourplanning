from db_connect_disconnect import DatabaseConnector
from orm import Tour, Address, Client
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

    def __init__(self, date, kolonne, strasse, hausnr, plz, ort, firmenname, info, private, zeitbedarf):
        """Initialisiert die DataWriter-Klasse."""
        self.db_connector = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
        self.session, _ = self.db_connector.get_session()
        log_config = LogConfig()
        self.logger = log_config.setup_logger('db_entry_log', 'db_entry.log')

        self.date = date
        self.kolonne = kolonne
        self.strasse = strasse
        self.hausnr = hausnr
        self.plz = plz
        self.ort = ort
        self.firmenname = firmenname
        self.info = info
        self.private = private
        self.zeitbedarf = zeitbedarf


    def create_db_entry(self):
        """Erstellt neue Einträge für Tour, Adresse und Kunde."""
        self.new_tour = Tour(date=self.date,
                        kolonne_type=self.kolonne,
                        private=self.private,
                        further_info=self.info,
                        zeitbedarf = self.zeitbedarf)
        
        self.new_address = Address(strasse=self.strasse,
                              hausnr=self.hausnr,
                              plz=self.plz,
                              ort=self.ort)
        
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

        self.new_client = Client(firmenname=self.firmenname)

        existing_client = self.session.query(Client).filter(and_(
             Client.firmenname == self.new_client.firmenname
        )).first()

        if existing_client:
             self.new_client = existing_client
        else:
             self.new_client = self.new_client

    def check_address(self):
        """Überprüft die Existenz einer Adresse und speichert sie in der Datenbank, falls gewünscht."""
        validator = BackgroundChecks(strasse=self.new_address.strasse,
                                     hausnr=self.new_address.hausnr,
                                     plz=self.new_address.plz,
                                     ort=self.new_address.ort)
        if validator.check_adress_existance():
                return True
        else:
            self.logger.error("Die Adresse existiert nicht und wird nicht in die DB geschrieben")
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
