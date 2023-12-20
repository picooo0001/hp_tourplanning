from flask import Flask, request, render_template, jsonify
from input_to_database import DataWriter
from orm import Tour, Address, Client
from db_connect_disconnect import DatabaseConnector
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

db_connection = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')

@app.route('/')
def index():
    return render_template('tours.html')

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

        if db_writer:
            return jsonify({'message': 'Tour successfully created!'})
        else:
            return jsonify({'message': 'Error creating tour!'}), 500


@app.route('/get_tours', methods=['GET'])
def get_tours():
    try:
        start_date_str = request.args.get('start')  # Nur das Startdatum als String aus der URL abrufen
        end_date_str = request.args.get('end')      # Nur das Enddatum als String aus der URL abrufen

        # Konvertiere das Start- und Enddatum von String zu DateTime
        start_date = datetime.fromisoformat(start_date_str.replace('T', ' '))
        end_date = datetime.fromisoformat(end_date_str.replace('T', ' '))

        # Sitzung für Datenbankoperationen erhalten
        db_session, connection_status = db_connection.get_session()

        # Daten aus der Datenbank abrufen und formatieren basierend auf dem Enddatum
        events = db_session.query(Tour, Address, Client)\
            .join(Client, Client.client_id == Tour.client_id)\
            .join(Address, Address.address_id == Tour.address_id)\
            .filter(Tour.date >= start_date, Tour.date <= end_date).all()

        formatted_tours = []
        for tour, address, client in events:
            formatted_tours.append({
                'title': f"{tour.kolonne_type} - {client.firmenname}",
                'start': tour.date.isoformat(),  # Datumsformat anpassen
                'description': f"Address: {address.strasse} {address.hausnr}, {address.plz} {address.ort}. Further Info: {tour.further_info}"
            })

        # Verbindung zur Datenbank schließen
        close_status, close_message = db_connection.close_connection()
        if not close_status:
            print("Fehler beim Schließen der Verbindung:", close_message)

        # Tour-Daten als JSON zurückgeben
        return jsonify(formatted_tours)
    
    except Exception as e:
        print("Fehler:", str(e))  # Hier kannst du den Fehler in der Konsole anzeigen
        return jsonify({'error': str(e)}), 500

    
if __name__ == '__main__':
    app.run(debug=True)