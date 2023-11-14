# Struktur
## Struktur Excel File:
- x: Aufbau Personen mit Kolonne, Abbau mit Kolonne, Umbau, Kolonne fehlt
- y: Tage 
- Inhalt: Firmenname, Adresse, besondere Termine (Staplerschein), zusätzl. Info

## Idee:
- Input (cli): 
    - 1. Wer? Welche Kolonne?, Welcher Tag? 
    - 2. Wo? Adresse, Firmenname, zustätzl. Info (**input validation**)
    - 3. Optionen um sachen zu ändern / rückgängig zu machen / bearbeiten
- Ausgabe (cli):
    - 1. Termine für bestimmten Tag auflisten
    - 2. insgesamte Anzeige (mit Filter nach Kolonne/ wichtige Personen)
- weitere Schritte:
    - 1. GUI
    - 2. Wo wird gespeichert? -> Datenbank / CSV Lokal
    - 3. von Punkt 2 abhängig: wie viele Benutzer?
    - 4. Login / PW?
    
- Checks:
    - 1. Adressen check mit api 