from flask import Flask, session, redirect, url_for, request, render_template, jsonify, send_from_directory
from werkzeug.security import check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
#from input_to_database import DataWriter
#from orm import Tour, Address, Client, User
#from db_connect_disconnect import DatabaseConnector
from datetime import datetime, timedelta, time
#from log_config import LogConfig
from sqlalchemy.orm import joinedload


#log_config = LogConfig()
#logger = log_config.setup_logger('flask_app.log', 'flask_app.log')

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
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zyzaedugpkirat:3ec08a08886f754a14800907a13c120e47ec177e761444db8a66cdadc1ea7a0c@ec2-3-217-146-37.compute-1.amazonaws.com:5432/dav0fmh2bi56a2'
app.secret_key = 'supersecretkey'

db = SQLAlchemy(app)

class Tour(db.Model):
    """Tabelle für Touren."""
    __tablename__ = 'tour'

    tour_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    address_id = db.Column(db.SmallInteger, db.ForeignKey('address.address_id'))
    client_id = db.Column(db.SmallInteger, db.ForeignKey('client.client_id'))
    date = db.Column(db.Date)
    kolonne_type = db.Column(db.VARCHAR(255))
    private = db.Column(db.VARCHAR(225))
    further_info = db.Column(db.VARCHAR(255))
    zeitbedarf = db.Column(db.Numeric(3,2))
    start_time = db.Column(db.Time)

    client = db.relationship("Client", back_populates="tours")
    address = db.relationship("Address")


    def __repr__(self):
        """Gibt eine lesbare Repräsentation der Tour-Tabelle zurück."""
        return f"<TourTable(id={self.tour_id}, kolonne_type={self.kolonne_type})>"

class Address(db.Model):
    """Tabelle für Adressen."""
    __tablename__ = 'address'

    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    strasse = db.Column(db.VARCHAR(255))
    hausnr = db.Column(db.VARCHAR(20))
    plz = db.Column(db.Integer)
    ort = db.Column(db.VARCHAR(100))

class Client(db.Model):
    """Tabelle für Kunden."""
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firmenname = db.Column(db.VARCHAR(255))
    
    tours = db.relationship("Tour")

class User(db.Model):
    """Tabelle für Login Daten"""
    __tablename__ = 'users'

    id = db.Column(db.nteger, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    """
    Zeigt die Startseite (Login Seite) der Webapp.

    Returns:
        str: HTML-Seite für die Startseite ('login_page.html').
    """
    return render_template('login_page.html')

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
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            #logger.info(session)
            return jsonify({'message': 'Anmeldung erfolgreich'}),200
        else:
            #logger.warning("Ungültige Anmeldeinformationen")
            return jsonify({'message': 'Ungültige Anmeldeinformationen'}), 401
    except Exception as e:
        #logger.error(e)
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
        #logger.info(session)
        return redirect(url_for('index'))
    except Exception as e:
        #logger.error(e)
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

        new_tour = Tour(
            date=date,
            kolonne_type=kolonne,
            further_info=info,
            private=private,
            zeitbedarf=zeitbedarf
        )

        new_address = Address(
            strasse=strasse,
            hausnr=hausnr,
            plz=plz,
            ort=ort
        )

        new_client = Client(
            firmenname = firmenname
        )

        db.session.add(new_tour)
        db.session.add(new_address)
        db.session.add(new_client)

        #logger.info("Tour successfully created!")
        return jsonify({'message': 'Tour successfully created!'})
            
    except Exception as e:
        #logger.error(e)
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

        events = db.session.query(Tour, Address, Client)\
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

        #logger.info(formatted_tours)
        return jsonify(formatted_tours)
    
    except Exception as e:
        #logger.error(e)
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
        tour = Tour.query.get(eventID)
        
        if tour:
            tour.zeitbedarf = new_duration
            db.session.commit()
            #logger.info("Event-Dauer erfolgreich aktualisiert")
            return jsonify({'message': 'Event-Dauer erfolgreich aktualisiert'})
        else:
            #logger.warning("Tour nicht gefunden")
            return jsonify({'error': 'Tour nicht gefunden'}), 404

    except Exception as e:
        #logger.error(e)
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
        tours = Tour.query.options(joinedload(Tour.client), joinedload(Tour.address)).all()
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
        #logger.info(serialized_tours)
        return jsonify(serialized_tours)
    
    except Exception as e:
        #logger.error(e)
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
        tour_to_delete = Tour.query.get(tour_id)

        if tour_to_delete:
            db.session.delete(tour_to_delete)
            db.session.commit()
            #logger.info(f'Tour mit ID {tour_id} wurde erfolgreich gelöscht.')
            return jsonify({'message': f'Tour mit ID {tour_id} wurde erfolgreich gelöscht.'}), 200
        else:
            #logger.warning(f'Tour mit ID {tour_id} nicht gefunden.')
            return jsonify({'error': f'Tour mit ID {tour_id} nicht gefunden.'}), 404
    
    except Exception as e:
        #logger.error(e)
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
        tour = Tour.query.get(tour_id)

        if tour:
            tour.kolonne_type = new_kolonne
            db.session.commit()
            #logger.info(f'Kolonne für Tour {tour_id} erfolgreich geändert')
            return jsonify({'message': f'Kolonne für Tour {tour_id} erfolgreich geändert'})
        else:
            #logger.warning(f'Tour mit ID {tour_id} nicht gefunden')
            return jsonify({'error': f'Tour mit ID {tour_id} nicht gefunden'}), 404
    except Exception as e:
        #logger.error(e)
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
        tour = Tour.query.get(eventID)

        if tour:
            tour.date = new_start_datetime.date()
            tour.start_time = new_start_datetime.time()
            db.session.commit()
            #logger.info(f'Tourdatum der Tour ID {eventID} erfolgreich aktualisiert')
            return jsonify({'message': f'Tourdatum der Tour ID {eventID} erfolgreich aktualisiert'})
        else:
            #logger.warning(f'Tour mit ID {eventID} nicht gefunden')
            return jsonify({'error': f'Tour mit ID {eventID} nicht gefunden'}), 404

    except Exception as e:
        #logger.error(e)
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

        tour = Tour.query.get(tour_id)

        if tour:
            address = tour.address
            if address:
                address.strasse = new_address['strasse']
                address.hausnr = new_address['hausnr']
                address.plz = new_address['plz']
                address.ort = new_address['ort']
                db.session.commit()
                #logger.info(f'Adresse der Tour mit der ID: {tour_id} erfolgreich geändert')
                return jsonify({'message': f'Adresse der Tour mit der ID: {tour_id} erfolgreich geändert'})
            else:
                #logger.warning(f'Adresse der Tour mit der ID: {tour_id} nicht gefunden')
                return jsonify({'error': f'Adresse der Tour mit der ID: {tour_id} nicht gefunden'}), 404
        else:
            #logger.warning(f'Adresse der Tour mit der ID: {tour_id} nicht gefunden')
            return jsonify({'error': f'Adresse der Tour mit der ID: {tour_id} nicht gefunden'}), 404

    except Exception as e:
        #logger.error(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
