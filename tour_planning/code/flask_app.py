from flask import Flask, request, render_template
from input_to_database import DataWriter
from db_connect_disconnect import DatabaseConnector

from orm import Tour  # Import your Tour model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('testseite.html')

@app.route('/create_tour', methods=['POST'])
def create_tour():
    if request.method == 'POST':
        # Daten aus dem Formular abrufen
        date = request.form['date']
        kolonne = request.form['kolonne']
        strasse = request.form['strasse']
        hausnr = request.form['hausnr']
        plz = request.form['plz']
        ort = request.form['ort']
        firmenname = request.form['firmenname']
        info = request.form['info']
        private = request.form['private']

        db_writer = DataWriter(date, kolonne, strasse, hausnr, plz, ort, firmenname, info, private)
        db_connector = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
        db_connector.get_session()
        db_writer.write_tour_data_to_db()

        return "Tour created successfully!"
    
@app.route('/tours')
def display_tours():
    try:
        # Create an engine to connect to your database
        engine = create_engine('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')

        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query the Tour table to fetch all tour data
        tours = session.query(Tour).all()

        # Close the session
        session.close()

        # Render a template and pass the fetched tour data to it
        return render_template('tours.html', tours=tours)

    except Exception as e:
        return render_template('error.html', error=str(e))

    

if __name__ == '__main__':
    app.run(debug=True)