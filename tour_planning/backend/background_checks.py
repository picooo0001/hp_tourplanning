import requests
import logging
from datetime import *

class BackgroundChecks:
    """
    Initialisiert einen AdresseValidator mit den angegebenen Adressinformationen.

    Args:
        strasse (str): Straßenname der Adresse.
        hausnr (str): Hausnummer der Adresse.
        plz (str): Postleitzahl der Adresse.
        ort (str): Ort der Adresse.
    """
    def __init__(self, strasse, hausnr, plz, ort):
        self.strasse = strasse
        self.hausnr = hausnr
        self.plz = plz
        self.ort = ort

        logging.basicConfig(filename='api_logs.log', level=logging.INFO)

    def check_adress_existance(self):
        """
        Überprüft die Existenz der angegebenen Adresse mithilfe der OpenStreetMap Nominatim API.

        Returns:
            bool: True, wenn die Adresse existiert; False, wenn die Adresse nicht existiert.
        """
        address = f"{self.strasse} {self.hausnr} {self.plz} {self.ort}"

        url = "https://nominatim.openstreetmap.org/search"

        params = {
            'format': 'json',
            'q': address
        }

        response = requests.get(url, params=params)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] Adresse: {address}, API-Antwort: {response.json()}, API-Statuscode: {response.status_code}"
        logging.info(log_message)

        if response.ok and len(response.json()) > 0:
            return True
        else:
            return False


        

