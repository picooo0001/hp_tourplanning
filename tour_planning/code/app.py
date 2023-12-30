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
#app.config['DATABASE_URL'] = 'postgres://hjosbvtqcidmbk:14c260d367e129e5d94221b2ba7ac414c72a969a561707ff8d680ce67264c65f@ec2-3-217-146-37.compute-1.amazonaws.com:5432/d317upfk639k0r'
app.secret_key = 'supersecretkey'

#db_connection = DatabaseConnector('postgresql://hp_admin:Nudelholz03#@localhost/hp_postgres')
#db_connection = DatabaseConnector(app.config['DATABASE_URL'])


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


if __name__ == '__main__':
    app.run(debug=True)