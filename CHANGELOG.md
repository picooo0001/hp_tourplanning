# Changelog
## 11.12.2023
- setup git repo
- started with simple backend logic

## 14.11.2023
- completed the user_input class for now

## 15.11.2023
- BackgroundChecks completed 
- created api_log
- TourCreation completed for now

## 16.11.2023
- installed PostgreSQL for testing
- wrote class DatabaseConnector which connects to db
- added new folder in tour_planning for db stuff
- created docker compose file for creting docker environment

## 07.12
- created Database
- rewrote DatabaseConnector
- added DatabaseDisconnector
- added orm.py with the database model
- added input_private to TourCreation
- started connecting all together (input_to_database.py)

## 8.12
- restructured folder
- continued working on input_to_database (still not fully working)
- updated (db_connect_disconnect) -> disconnect class not fully working

## 9.12
- finished input_to_database (fully working now with address check)
- fixed DBConnector (fully working now)
- restructured "log policy" meaning created new class for log management -> each function which writes into logfiles writ
- deleted unnecessary code

## 10.12.2023
- replaced the user_inputs (TourCreation) by flask_app -> for the web application
- constructed a check, that the same "Firmenname" doesnt get listed twice in the DB
- restructured the folder
- added TODO.md to track open To Do's
- adapted the input_to_database file so the data comes from the flask app now, not anymore from the TourCreation

## 14.12.2023
- rewrote some code in py classes
- created and designed the tourcreations.html
- added responses without redirecting
- finished the tourcreations.html

## 20.12.2023
- got calendar working
- flask has now a route (get_tours) which displays the tours in a FullCalendar