from flask import Flask, request, render_template
from input_to_database import DataWriter
from db_connect_disconnect import DatabaseConnector
from orm import Tour

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

if __name__ == '__main__':
    app.run(debug=True)