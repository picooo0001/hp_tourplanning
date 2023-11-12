from datetime import datetime, timedelta

class TourCreation:
    """
    Eine Klasse, die durch UserInput einen Auftrag anlegt.

    Attribute:
        date (date): Datum für die Tour
        kolonne (str): Name der Kolonne die den Auftrag ausführt
        person (str): Person, die für die Kolonne verantwortlich ist
        strasse (str): Straßenname, wo der Auftrag ausgeführt wird
        hausnr (int): Hausnummer zum Straßenname
        plz (int): Postleihzahl
        ort (str): Ort
        firmenname (str): Name der Firma, die den Auftrag bestellt
        info (str): zustätliche Info
    """

    def __init__(self):
        """
        Initialisiert einen neuen Auftrag

        Args: 
            s.o
        """
        self.date = None
        self.kolonne = None
        self.person = None
        self.strasse = None
        self.hausnr = None
        self.plz = None
        self.ort = None
        self.firmenname = None
        self.info = None
    
    def date_input(self):
        """
         Fordert den Benutzer auf, ein Datum im Format DD/MM/YYYY einzugeben.
        Validiert die Eingabe auf Realismus (nicht in der Vergangenheit, nicht mehr als 1 Jahr in der Zukunft).

        Returns:
        datetime: Das eingegebene und validierte Datum als datetime-Objekt.
        """
        while True:
            user_input = input("Bitte gebe das Datum in Format DD/MM/YYYY ein:")

            try:
                # Versuch, das Datum zu parsen
                cleaned_input = user_input.replace(".","/").replace(",","/")
                date_object = datetime.strptime(cleaned_input,"%d/%m/%Y")

                if date_object < datetime.now():
                    # Liegt Datum in der Vergangenheit?
                    print("Das eingegebene Datum liegt in der Vergangenheit. Bitte überprüfen")
                elif date_object > datetime.now() + timedelta(days=365):
                    # Liegt Datum in der Zukunft?
                    print("Das eingegebene Datum liegt zu weit in der Zukunft. Bitte überprüfen")
                else:
                    # Gültiger Input, Datum wird ausgegeben
                    self.date = date_object
                    return date_object
            except ValueError:
                # Fehler bei Datumsvalidierung
                print("Ungültiges Datum. Bitte Format DD/MM/YYY verwenden")        

if __name__ == "__main__":
    tourcreation = TourCreation()
    #selected_date = tourcreation.date_input()
    #print(f"Das ausgewählte und validierte Datum ist: {selected_date.strftime('%d/%m/%Y')}")

