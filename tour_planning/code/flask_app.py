from flask import Flask, request, render_template, jsonify
from input_to_database import DataWriter
from orm import Tour, Address, Client
from db_connect_disconnect import DatabaseConnector
from datetime import datetime, timedelta, time
from sqlalchemy.orm import class_mapper, joinedload

def to_dict(model):
    """Konvertiert eine SQLAlchemy-Instanz in ein JSON-serialisierbares Dictionary."""
    columns = [str(c).split('.')[1] for c in model.__table__.columns]
    return dict((c, getattr(model, c)) for c in columns)

app = Flask(__name__, static_folder='static')

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
        zeitbedarf = request.form['zeitbedarf']

        db_writer = DataWriter(date, kolonne, strasse, hausnr, plz, ort, firmenname, info, private, zeitbedarf)
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

            kolonne_color_map = {
                'Kolonne A': 'red',
                'Kolonne B': 'green',
                # Weitere Kolonnen und deren Farben
            }

            kolonne = tour.kolonne_type  # Annahme: Die Eigenschaft, die die Kolonne angibt
            event_color = kolonne_color_map.get(kolonne, 'blue')

            event_date = tour.date
            event_start = datetime.combine(event_date, time(7,0,0))
            event_duration = float(tour.zeitbedarf) if tour.zeitbedarf is not None else 1.0
            event_end = event_start + timedelta(hours=event_duration * 8)
            
            formatted_tours.append({
                'id': tour.tour_id,
                'title': f"{kolonne}",
                'start': event_start.isoformat(),
                'end': event_end.isoformat(),
                'allDay': False,
                'backgroundColor': event_color,
                'description': f"{client.firmenname} <br> {address.strasse} {address.hausnr} <br> {address.ort} <br> {address.plz} <br> {tour.further_info}"
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
    
@app.route('/show_tours', methods=['GET'])
def show_tours():
    db_session, connection_status = db_connection.get_session()
    tours = db_session.query(Tour).options(joinedload(Tour.client)).all()
    serialized_tours = [
        {
            'tour_id': tour.tour_id,
            'date': tour.date,
            'kolonne_type': tour.kolonne_type,
            'firmenname': tour.client.firmenname if tour.client else None
        }
        for tour in tours
    ]
    return jsonify(serialized_tours)

@app.route('/delete_tour/<int:tour_id>', methods=['DELETE'])
def delete_tour(tour_id):
    try:
        db_session, connection_status = db_connection.get_session()

        # Suche die Tour anhand der ID
        tour_to_delete = db_session.query(Tour).filter_by(tour_id=tour_id).first()

        if tour_to_delete:
            # Lösche die Tour
            db_session.delete(tour_to_delete)
            db_session.commit()

            return jsonify({'message': f'Tour mit ID {tour_id} wurde erfolgreich gelöscht.'}), 200
        else:
            return jsonify({'error': f'Tour mit ID {tour_id} nicht gefunden.'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/change_kolonne/<int:tour_id>/<new_kolonne>', methods=['PUT'])
def change_kolonne(tour_id, new_kolonne):
    try:
        db_session, connection_status = db_connection.get_session()

        tour = db_session.query(Tour).filter_by(tour_id=tour_id).first()
        if tour:
            tour.kolonne_type = new_kolonne
            db_session.commit()
            return jsonify({'message': f'Kolonne für Tour {tour_id} erfolgreich geändert'})
        else:
            return jsonify({'error': f'Tour mit ID {tour_id} nicht gefunden'}), 404
    except Exception as e:
        print("Fehler:", str(e))
        return jsonify({'error': str(e)}), 500
    
@app.route('/update_date/<int:eventID>', methods=['POST'])
def update_date(eventID):
    try: 
        data = request.json
        new_date = data.get('newDate')

        db_session, connection_status = db_connection.get_session()

        tour = db_session.query(Tour).filter_by(tour_id=eventID).first()
        if tour:
            tour.date = new_date
            db_session.commit()
            return jsonify({'message': 'Tourdatum erfolgreich aktualisiert'})
        else:
            return jsonify({'error': 'Tour nicht gefunden'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)