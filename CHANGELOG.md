# Changelog
## 11.11.2023
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

## 22.12.2023 
- started working on date drag and drop function. Works but date doesnt get updated in Database.
- Updated few things on calendar

## 24.12.2023
- added "zeitbedard" in tourcreation and updated database / database model etc.
- added "zeitbedarf" to flask route so the events have a specified length (there have always been all-day)
- customized the calendar

## 26.12.2023
- added popup to tourcreation (success/fail)
- updated calendar: day view, week view, for an better overview
- adapted some other things like start end time and how the events get displayed

## 27.12.2923
- created modify_tours (site where the user can modify the tours)
- created a tour list inside the modify_tours file
- created delete and change kolonne button for the list
- implemented drag n drop function in the calendar so user can change the date by dragging and dropping

## 28.12.2023
- impelemted a function to change the date (inclusive flask route etc.)
- adapted the database model for adress (now the adress shows up as well in modify_tours list)
- prettied up the code of modify_tours with bootstrap
- linked up the different html sites amongst each other
- added Login Page with login logic (user / hashed pw is stored in db) - access thourgh flask route
- added logout function - in navbar of each site
- added protection to the sites meaning that you cant see content / send content without signing in
- added new table for user auth in db (adaptedt database model as well)

## 30.12.2023
- added new Column to database (start_time) / adapted the database model
- added a popup to the login page (if your credentials are wrong)
- added functionality to change the start- and endtime of events
- added functionality to change the event duration