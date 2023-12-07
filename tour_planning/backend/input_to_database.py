from db_connect_disconnect import DatabaseConnector
from db_connect_disconnect import DatabaseDisconnector
from orm import Tour, Address, Client
from user_input import TourCreation

class DataWriter:
    def __init__(self):
        self.db_connector = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
        self.db_disconnector = DatabaseDisconnector()
        self.tourcreation = TourCreation()

    def write_tour_data_to_db(self):
        session, _ = self.db_connector.get_session()

        #new_tour = Tour(date=self.tourcreation.date_input(), 
                        #kolonne_type=self.tourcreation.kolonne_input(),
                        #private=self.tourcreation.input_private(),
                        #further_info=self.tourcreation.input_info())
        
        new_address = Address(strasse=self.tourcreation.input_strasse(),
                              hausnr=self.tourcreation.input_hausnr(),
                              plz=self.tourcreation.input_plz(),
                              ort=self.tourcreation.input_ort())
        
        new_client = Client(firmenname=self.tourcreation.input_firmenname())

        session.add(new_client)
        #session.flush()
        session.add(new_address)
        #session.flush()
        #session.add(new_tour)
        session.commit()
        print(new_client.client_id)
        print(new_address.address_id)
        self.db_disconnector.close_connection()


if __name__ == "__main__":
    db_connector = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
    establish_connection = db_connector.get_session()

    #tourcreation = TourCreation()

    db_writer = DataWriter()
    db_writer.write_tour_data_to_db()









