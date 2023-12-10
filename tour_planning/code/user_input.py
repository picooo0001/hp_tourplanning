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
        self.firmenname = None
        self.strasse = None
        self.hausnr = None
        self.plz = None
        self.ort = None
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

    def input_strasse(self):
        """
        Fordert den Benutzer auf, einen Straßennamen einzugeben und überprüft den Input mit der Klasse 'BackgroundCheck'

        Returns:
        str: Der eingegebene Straßenname.
        """

        while True:
            strasse_input = str(input("Bitte gebe den Straßenname ein:"))
            if strasse_input.isalpha():
                    self.strasse = strasse_input.capitalize()
                    return strasse_input
            else:
                print("Fehler: Ungültige Einagbe. Nur Buchstaben hier.")

    def input_hausnr(self):
        """
        Fordert den Benutzer auf, eine Hausnummer einzugeben.
        Validiert die Eingabe auf Realismus (keine Buchstaben, keine negativen Werte, keine Werte über 500).

        Returns:
        int: Die eingegebene und validierte Hausnummer.
        """

        while True:
            hausnummer_input = input("Bitte gebe die Hausnummer ein: ")

            if not hausnummer_input:
                print("Ungültige Eingabe. Bitte geben Sie eine Hausnummer ein.")
                continue

            if hausnummer_input.isdigit() or (hausnummer_input.count('/') == 1 and all(part.isdigit() for part in hausnummer_input.split('/'))):
                hausnummer = eval(hausnummer_input)  # Hier wird der Ausdruck ausgewertet
                if 0 < hausnummer <= 500:
                    # Gültige Eingabe, Hausnummer wird ausgegeben
                    self.hausnr = hausnummer_input
                    return hausnummer_input
                else:
                    print("Ungültige Eingabe. Bitte überprüfe die Eingabe.")
            else:
                print("Ungültige Eingabe. Bitte geben Sie eine gültige Hausnummer ein.")

    def input_plz(self):
       """
        Fordert den Benutzer auf, eine Postleitzahl einzugeben.
        Validiert die Eingabe auf Realismus (nicht länger als 5 Stellen).

        Returns:
            str: Die eingegebene und validierte Postleitzahl.
        """ 

       while True:
           plz_input = input("Bitte gebe die Postleihzahl ein:") 
           
           if len(plz_input) == 5 and plz_input.isdigit():
               self.plz = plz_input
               return plz_input
           else:
               print("Ungültige Eingabe. Überprüfe die Länge deiner Postleihzahl. Es dürfen auch keine Buchstaben enthalten sein.")

    def input_ort(self):
        """
        Fordert den Benutzer auf, einen Ort einzugeben.
        Validiert die Eingabe auf Realismus (keine Zahlen, erlaubte Zeichen, erster Buchstabe großgeschrieben, nicht leer).

        Returns:
            str: Die eingegebene und validierte Ortsangabe.
        """
        ort_input = input("Bitte geben Sie den Ort oder die Stadt ein: ")

        if ort_input.strip() and not any(char.isdigit() for char in ort_input) and all(char.isalpha() or char in "- " for char in ort_input):
            self.ort = ort_input.title()
            return ort_input.title()
        elif ort_input == "":
            raise RuntimeError("Ort darf nicht leer gelassen werden.")
        else:
            print("Ungültige Eingabe. Der Ort sollte keine Zahlen enthalten und erlaubte Zeichen wie '-' können verwendet werden.")      

    def input_firmenname(self):
        """
        Fordert den Benutzer auf, einen Firmennamen einzugeben.
        Validiert die Eingabe auf Realismus (erster Buchstabe großgeschrieben).

        Returns:
            str: Die eingegebene und validierte Firmenbezeichnung.
        """

        while True:
            firmenname_input = input("Bitte gebe den Namen des Auftraggebers ein: ")

            if firmenname_input.strip() and all(char.isalnum() or char.isspace() or char in "-_.,;:()[]" for char in firmenname_input):
                self.firmenname = firmenname_input.title()
                return firmenname_input.title()  
            else:
                print("Ungültige Eingabe. Der Firmenname sollte nicht leer sein und erlaubte Zeichen wie Zahlen, Buchstaben, Leerzeichen und einige Sonderzeichen können verwendet werden.")
    
    def input_private(self):
        """
        Fordert den Benutzer auf, anzugeben ob es sich um einen Privatkunden handelt.
        Validiert die Eingabe auf Realismus (Ja / Nein -> True / False).

        Returns:
            bool: true, false
        """

        while True:
            private_input = input("Handelt es sich um eine Privatperson: ").strip().lower()

            if private_input == "ja":
                self.private = True
                return True
            elif private_input == "nein":
                self.private = False
                return False
            else:
                print("Ungültige Eingabe. Bitte Ja / Nein eingeben.")
    def input_info(self):
        """
        Fordert den Benutzer auf, zusätzliche Informationen einzugeben.

        Returns:
        str: Die eingegebenen und validierten zusätzlichen Informationen.
        """
        info_input = input("Bitte geben Sie zusätzliche Informationen ein (optional): ")
        self.info = info_input.title()
        return info_input.title()
    
    def ask_user_to_save_input(self):
        """
        Fragt den Benutzer, ob er die Adresse mit Kolonne, Datum, Firma und Info in die Datenbank speichern möchte.

        Returns:
            bool: True, wenn der Benutzer speichern möchte; False, wenn nicht.
        """
        user_input = str(input("Möchten Sie die Adresse mit Kolonne, Datum und Firma in die Datenbank speichern? (Ja/Nein): "))
        return user_input.lower() == "ja"


