from flask import Flask, session, redirect, url_for, request, render_template, jsonify, send_from_directory
from werkzeug.security import check_password_hash
from sqlalchemy.orm import joinedload
from functools import wraps
from input_to_database import DataWriter
from orm import Tour, Address, Client, User
from db_connect_disconnect import DatabaseConnector
from datetime import datetime, timedelta, time
from log_config import LogConfig

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

log_config = LogConfig()
logger = log_config.setup_logger('flask_app.log', 'flask_app.log')

def login_required(route_function):
    """Diese Methode sorgt dafür, dass die Endpoints geschützt werden und nicht ohne Anmeldung darauf zugegriffen werden kann."""
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:  
            return redirect(url_for('index')) 
        return route_function(*args, **kwargs)
    return decorated_function

def to_dict(model):
    """Konvertiert eine SQLAlchemy-Instanz in ein JSON-serialisierbares Dictionary. War wichtig um die Touren in der Toureinträge bearbeiten Unterseite, anzeigen zu können."""
    columns = [str(c).split('.')[1] for c in model.__table__.columns]
    return dict((c, getattr(model, c)) for c in columns)

app = Flask(__name__, static_folder='static')
app.config['DATABASE_URL'] = 'postgres://hjosbvtqcidmbk:14c260d367e129e5d94221b2ba7ac414c72a969a561707ff8d680ce67264c65f@ec2-3-217-146-37.compute-1.amazonaws.com:5432/d317upfk639k0r'
app.secret_key = 'supersecretkey'

engine = create_engine(app.config['DATABASE_URL'])
Session = sessionmaker(bind=engine)

#db_connection = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
#db_connection = DatabaseConnector(app.config['DATABASE_URL'])



@app.route('/')
def index():
    """
    Zeigt die Startseite (Login Seite) der Webapp.

    Returns:
        str: HTML-Seite für die Startseite ('login_page.html').
    """
    try:
        session = Session()
        message = "Verbindung erfolgreich hergestellt."
        logger.info(message)
        # Führe hier Datenbankoperationen mit 'session' aus
        return render_template('login_page.html')
    except Exception as e:
        message = f"Fehler beim Verbindungsaufbau: {str(e)}"
        logger.error(message)
        return f"Fehler: {str(e)}"


@app.route('/<path:filename>')
def send_html(filename):
    """
    War dafür, um die verschiedenen Unterseiten über die Navbar zu verlinken.

    Args:
        filename (str): Name der Datei, die gesendet werden soll.

    Returns:
        file: Die angeforderte Datei aus dem 'templates'-Ordner.
    """
    return send_from_directory('templates', filename)

@app.route('/login', methods=['POST'])
def login():
    """
    Bearbeiter den Login des Benutzers.

    Returns:
        JSON: Meldung, ob der Login erfolgreich war oder nicht.
    """
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        db_session, connection_status = db_connection.get_session()
        user = db_session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            logger.info(session)
            return jsonify({'message': 'Anmeldung erfolgreich'}),200
        else:
            logger.warning("Ungültige Anmeldeinformationen")
            return jsonify({'message': 'Ungültige Anmeldeinformationen'}), 401
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    """
    Loggt den Benutzer aus seiner momentanen Session aus.

    Returns:
        redirect: leitet den Nutzer zur Login Page.
    """
    try:
        session.pop('logged_in', None)
        logger.info(session)
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/create_tour', methods=['POST'])
@login_required
def create_tour():
    """
    Erstellt eine neue Tour, die auf den Usereingaben basiert.

    Returns:
        JSON: Status der Tourcreation
    """
    try:
        if request.method == 'POST':
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

            db_writer = DataWriter(date, kolonne, strasse, hausnr, plz, ort, firmenname, info, private, zeitbedarf, start_time="08:00:00")
            db_connector = DatabaseConnector(app.config['DATABASE_URL'])
            db_connector.get_session()
            db_writer.write_tour_data_to_db()
            db_connector.close_connection()

            if db_writer:
                logger.info("Tour successfully created!")
                return jsonify({'message': 'Tour successfully created!'})
            else:
                logger.warning("Error creating tour!")
                return jsonify({'message': 'Error creating tour!'}), 500
            
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500


@app.route('/get_tours', methods=['GET'])
@login_required
def get_tours():
    """
    Ruft alle existierenden Touren auf und stellt sich im Anschluss im Kalender dar.

    Returns:
        JSON: Liste der formtierten Tourdaten für die Darstellung als Kalendereintrag.
    """
    try:
        start_date_str = request.args.get('start')  
        end_date_str = request.args.get('end')      

        start_date = datetime.fromisoformat(start_date_str.replace('T', ' '))
        end_date = datetime.fromisoformat(end_date_str.replace('T', ' '))

        db_session, connection_status = db_connection.get_session()

        events = db_session.query(Tour, Address, Client)\
            .join(Client, Client.client_id == Tour.client_id)\
            .join(Address, Address.address_id == Tour.address_id)\
            .filter(Tour.date >= start_date, Tour.date <= end_date).all()

        formatted_tours = []
        for tour, address, client in events:

            kolonne_color_map = {
                'Kolonne A': 'red',
                'Kolonne B': 'green',
                # Bei Bedarf weitere Kolonnen hinzufügen!
            }

            kolonne = tour.kolonne_type
            event_color = kolonne_color_map.get(kolonne, 'blue')

            start_time = tour.start_time
            event_date = tour.date
            event_start = datetime.combine(event_date, start_time)
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

        close_status, close_message = db_connection.close_connection()
        if not close_status:
            logger.error(close_message)
            print("Fehler beim Schließen der Verbindung:", close_message)
        logger.info(formatted_tours)
        return jsonify(formatted_tours)
    
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/update_duration/<int:eventID>', methods=['POST'])
@login_required
def update_duration(eventID):
    """
    Aktualisiert die Dauer einer Tour auf Angabe der Nutzer

    Args:
        eventID (int): Tour ID
    
    Returns:
        JSON: Status der DB Aktualisierung
    """
    try:
        data = request.json
        new_duration = float(data.get('newDuration'))

        db_session, connection_status = db_connection.get_session()

        tour = db_session.query(Tour).filter_by(tour_id=eventID).first()
        if tour:
            tour.zeitbedarf = new_duration
            db_session.commit()
            logger.info("Event-Dauer erfolgreich aktualisiert")
            return jsonify({'message': 'Event-Dauer erfolgreich aktualisiert'})
        else:
            logger.warning("Tour nicht gefunden")
            return jsonify({'error': 'Tour nicht gefunden'}), 404

    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/show_tours', methods=['GET'])
@login_required
def show_tours():
    """
    Zeigt alle Touren in der Unterseite Toureinträge bearbeiten.

    Returns:
        JSON: Liste aller Touren und ihrer Details.
    """
    try: 
        db_session, connection_status = db_connection.get_session()
        tours = db_session.query(Tour).options(joinedload(Tour.client), joinedload(Tour.address)).all()
        serialized_tours = [
            {
                'tour_id': tour.tour_id,
                'date': tour.date,
                'kolonne_type': tour.kolonne_type,
                'firmenname': tour.client.firmenname if tour.client else None,
                'strasse': tour.address.strasse if tour.address else None,
                'hausnr': tour.address.hausnr if tour.address else None,
                'plz': tour.address.plz if tour.address else None,
                'ort': tour.address.ort if tour.address else None
            }
            for tour in tours
        ]
        logger.info(serialized_tours)
        return jsonify(serialized_tours)
    
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/delete_tour/<int:tour_id>', methods=['DELETE'])
@login_required
def delete_tour(tour_id):
    """
    Löscht eine Tour anhand der ID

    Args:
        tour_id (int): Die Tour ID
    
    returns:
        JSON: Status der Löschung
    """
    try:
        db_session, connection_status = db_connection.get_session()
        tour_to_delete = db_session.query(Tour).filter_by(tour_id=tour_id).first()

        if tour_to_delete:
            db_session.delete(tour_to_delete)
            db_session.commit()
            logger.info(f'Tour mit ID {tour_id} wurde erfolgreich gelöscht.')
            return jsonify({'message': f'Tour mit ID {tour_id} wurde erfolgreich gelöscht.'}), 200
        else:
            logger.warning(f'Tour mit ID {tour_id} nicht gefunden.')
            return jsonify({'error': f'Tour mit ID {tour_id} nicht gefunden.'}), 404
    
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/change_kolonne/<int:tour_id>/<new_kolonne>', methods=['PUT'])
@login_required
def change_kolonne(tour_id, new_kolonne):
    """
    Ändert die Spalte 'Kolonne' in der Datenbank.

    Args:
        tour_id (int): Tour ID
        new_kolonne (str): Name der Kolonne

    Returns:
        JSON: Status der Änderung 
    """
    try:
        db_session, connection_status = db_connection.get_session()
        tour = db_session.query(Tour).filter_by(tour_id=tour_id).first()
        
        if tour:
            tour.kolonne_type = new_kolonne
            db_session.commit()
            logger.info(f'Kolonne für Tour {tour_id} erfolgreich geändert')
            return jsonify({'message': f'Kolonne für Tour {tour_id} erfolgreich geändert'})
        else:
            logger.warning(f'Tour mit ID {tour_id} nicht gefunden')
            return jsonify({'error': f'Tour mit ID {tour_id} nicht gefunden'}), 404
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/update_event/<int:eventID>', methods=['POST'])
@login_required
def update_event(eventID):
    """
    Aktualisiert Datum und Startzeit des Events.

    Args:
        eventID (int): Tour ID
    
    Returns:
        JSON: Status der Änderung
    """
    try: 
        data = request.json
        new_start = data.get('newStart')

        new_start_datetime = datetime.fromisoformat(new_start)

        db_session, connection_status = db_connection.get_session()

        tour = db_session.query(Tour).filter_by(tour_id=eventID).first()
        if tour:
            tour.date = new_start_datetime.date()  # Datum aktualisieren
            tour.start_time = new_start_datetime.time()
            db_session.commit()
            logger.info(f'Tourdatum der Tour ID {eventID} erfolgreich aktualisiert')
            return jsonify({'message': f'Tourdatum der Tour ID {eventID} erfolgreich aktualisiert'})
        else:
            logger.warning(f'Tour mit ID {eventID} nicht gefunden')
            return jsonify({'error': f'Tour mit ID {eventID} nicht gefunden'}), 404

    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500

    
@app.route('/change_address/<int:tour_id>', methods=['PUT'])
@login_required
def change_address(tour_id):
    """
    Aktualisiert die Adresse einer Tour

    Args: 
        eventID (int): die Tour ID

    Returns:
        JSON: Status der Änderung
    """
    try:
        data = request.json
        new_address = data.get('newAddress')

        strasse = new_address.get('strasse')
        hausnr = new_address.get('hausnr')
        plz = new_address.get('plz')
        ort = new_address.get('ort')

        db_session, connection_status = db_connection.get_session()
        tour = db_session.query(Tour).filter_by(tour_id=tour_id).first()

        if tour:
            address = db_session.query(Address).filter_by(address_id=tour.address_id).first()
            if address:
                address.strasse = new_address['strasse']
                address.hausnr = new_address['hausnr']
                address.plz = new_address['plz']
                address.ort = new_address['ort']
                db_session.commit()
                db_session.close()
                logger.info(f'Adresse der Tour mit der ID: {tour_id} erfolgreich geändert')
                return jsonify({'message': f'Adresse der Tour mit der ID: {tour_id} erfolgreich geändert'})
            else:
                db_session.close()
                logger.warning(f'Adresse der Tour mit der ID: {tour_id} nicht gefunden')
                return jsonify({'error': f'Adresse der Tour mit der ID: {tour_id} nicht gefunden'}), 404
        else:
            db_session.close()
            logger.warning(f'Adresse der Tour mit der ID: {tour_id} nicht gefunden')
            return jsonify({'error': f'Adresse der Tour mit der ID: {tour_id} nicht gefunden'}), 404

    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)