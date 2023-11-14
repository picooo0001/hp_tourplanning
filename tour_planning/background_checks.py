import requests

class BackgroundChecks:
    """
    Diese Klasse überprüft im Hintergrund on die eingegebenen Werte stimmen können.

    Args:
        strasse (str): Der zu überprüfende Straßenname
    
    Returns:
        bool: True, wenn die Straße existiert, sonst False
    """
    @staticmethod
    def check_userinput_strasse(strasse):
        
        url = 'https://nominatim.openstreetmap.org/search'
        parameter = {
            "format": "json",
            "street": strasse,
            "limit": 3
        }

        response = requests.get(url, params=parameter)
        data = response.json

        print("Inhalt von response.json():", response.json())

