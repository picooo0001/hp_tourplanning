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

    def kolonne_input(self):
        """
        Fordert den Benutzer auf, eine Kolonne aus vordefinierten Werten auszuwählen.

        Return:
            str: Der ausgewählte Wert (Kolonne + Verantwortlicher)
        """
        vordefinierte_kolonnen = ["Kolonne Ferat - Hardy", "Kolonne Driton - Heni", "Kolonne Argon - Uwe", "Kolonne Benni - Ivan", "Kolonne Bogdan - Marius", "Kolonne Adrian - ???" , "Kolonne Alin - ??? ", "Kolonne Daniel - ??? ", "Kolonne Sabit - ???", "Kolonne Sabit - ???"]
        
        while True:
            
            print("Verfügbare Werte:")
            for index, value in enumerate(vordefinierte_kolonnen, start=1):
                print(f"{index}. {value}")
            
            user_input = int(input("Bitte Wert zwischen 1 - 10 eingeben:"))

            try: 
                index = user_input
                if 1 <= index <= len(vordefinierte_kolonnen):
                    selected_kolonne = vordefinierte_kolonnen[index - 1]
                    self.kolonne = selected_kolonne
                    return selected_kolonne
            # nicht ganz funktional -> später überprüfen (keine Beeinträchtigung)
            except (ValueError, IndexError):
                print("Ungültige Eingabe. Bitte gebe eine Zahl zwischen 1 und 10 ein.")
                continue
                        

if __name__ == "__main__":
    tourcreation = TourCreation()
    #selected_date = tourcreation.date_input()
    #print(f"Das ausgewählte und validierte Datum ist: {selected_date.strftime('%d/%m/%Y')}")
    #selected_kolonne = tourcreation.kolonne_input()
    #print(f"Der ausgewählte Wert ist: {selected_kolonne}")
    #print(f"Der ausgewählte Wert wurde in self.kolonne gespeichert: {tourcreation.kolonne}")

