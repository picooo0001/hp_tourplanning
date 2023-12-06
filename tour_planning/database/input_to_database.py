from db_connect_disconnect import DatabaseConnector
from db_connect_disconnect import DatabaseDisconnector
from tour_planning.user_input import TourCreation
from orm import Tour, Address, Client

class DataWriter:
    def __init__(self):
        self.db_connector = DatabaseConnector()
        self.db_disconnector = DatabaseDisconnector()
        self.tourcreation = TourCreation()


    def write_tour_data_to_db(self):
        session, _ = self.db_connector.get_session()

        new_tour = Tour(date=self.tourcreation.date_input(), 
                        kolonne_type=self.tourcreation.kolonne_input(),
                        private=self.tourcreation.input_private(),
                        further_info=self.tourcreation.input_info())
        
        new_address = Address(strasse=self.tourcreation.input_strasse(),
                              hausnr=self.tourcreation.input_hausnr(),
                              plz=self.tourcreation.input_plz(),
                              ort=self.tourcreation.input_ort())
        
        new_client = Client(firmenname=self.tourcreation.input_firmenname())

        session.add(new_client)
        session.add(new_address)
        session.add(new_tour)
        session.commit()
        self.db_disconnector.close_connection()

if __name__ == "__main__":
    db_connector = DatabaseConnector()
    establish_connection = db_connector.get_session()

    tourcreation = TourCreation()

    db_writer = DataWriter()
    db_writer.write_tour_data_to_db()









