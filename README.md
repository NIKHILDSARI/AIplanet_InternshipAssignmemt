AIplanet_Internshipassignmemt :-

Postgres CLI -

connect to Postgres and create database

			psql -U postgres_username 
    
 			CREATE DATABASE AIplanetassignmentDB;
    
Creating Django project -

		pipenv install django

		django-admin startproject Hackathon .

		django-admin startapp  Hackathon_api
	
Sending POST and GET request - used POSTMAN
    
Endpoints -

1) create_hackathon/ - (POST) Endpoint for creating a new Hackathon. This API can only be accessed by authorized users who provide their credentials.

2) uploadsubmission/ - (POST) Endpoint for participants to upload their submissions. This API can only be accessed by participants
 			who provide their credentials. The API validates the participant's submission based on its type. For file submissions, it checks for empty 			   files.For link submissions, it checks for valid links.

3) registration/ - (POST) Endpoint for participants to register for a particular hackathon.

4) enrolledlist/ - (POST) Endpoint to get a list of all the hackathons in which a participant is enrolled.

5) allsubmissions/ - (POST) Endpoint to get a list of all the submissions of a participant.

6) listofhackathons/ - (GET) Endpoint to get a list of hackathons created by an authorized user.

7) clickonsubmission/ - (POST) Endpoint to get the data of a particular hackathon when clicked.

8) favouritesubmissions/ - (POST) Endpoint to get all the favourite submissions of a participant.

Methods used -

loads method from json module to fetch data from request body

serialize method from serializers module to serialize querysets to required formates

