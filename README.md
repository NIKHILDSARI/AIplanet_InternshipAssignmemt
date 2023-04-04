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

 create_hackathon/  
 	
	Description: (POST) Endpoint for creating a new Hackathon. This API can only be accessed by authorized users
		      who provide their credentials.
	
	Inputs :-
	
	hackathon: {
    			"title": "HCL Volt MX Hackathon 2023",
  			"description":  " Configurable e-commerce app E-commerce applications have multiple micro-apps that work together or create a 
   			          larger application.Some of these micro-apps include authentication, inventory management,payments, and delivery, just to name				          a few. This app can also be configured for different domains in e-commerce such as clothes and electronics.",
    			"submission_type":"file",
    			"start_date":"Mar 14, 2023",
    			"end_date":"May 15, 2023",
    			"reward_prize":"USD 7000",
    			"github_repository":"https://github.com/NIKHILDSARI/",
    			"other_links": "primus.dasari@gmail.com
    	}
	
    	credentials : {
    			"username": "nikhil1234",
    			"password": "nikhil1234"
		}



 uploadsubmission/ - 


		Description: (POST) Endpoint for participants to upload their submissions. This API can only be accessed by participants
 			     who provide their credentials. The API validates the participant's submission based on its type. For file submissions, it checks for empty 			     files.For link submissions, it checks for valid links.
			  
		submission:  	{
   					"enrolled_hackathon":"HCL Volt MX Hackathon 2023",
					"submission_name":"submission_name",
					"submission_summary":"submission_summary",
					"challenge":"https://github.com/NIKHILDSARI/",
					"favourite":"true"
        
        			}
				
		credentials:   {
    					"username": "test_user1",
    					"password": "samtron555v"
				}


registration/ - 

		Description: (POST) Endpoint for participants to register for a particular hackathon.
		
		Registration: {
					"enrolled_to":"akhil Volt MX Hackathon 2023",
					"participant_name" : "participant_name",	
					"email":"primus.dasari@gmail.com"
		}
		
		credentials: {
    					"username": "test_user1",
    					"password": "samtron555v"
				}


enrolledlist/ - 

		Description: (POST) Endpoint to get a list of all the hackathons in which a participant is enrolled.
		
		credentials : {
    					"username": "test_user1",
   				 	"password": "samtron555v"
				}
				
				
allsubmissions/ - 

		Description: (POST) Endpoint to get a list of all the submissions of a participant.
		credentials : {
   					 "username": "test_user1",
   					 "password": "samtron555v"
				}

 listofhackathons/ - 
 
 		Description: (GET) Endpoint to get a list of hackathons created by an authorized user.
		
		
 clickonsubmission/ - 
 
 		Description: (POST) Endpoint to get the data of a particular hackathon when clicked.
		
		title : {
				"title":"wipro Volt MX Hackathon 2023"
			}

favouritesubmissions/ - 

		Description: (POST) Endpoint to get all the favourite submissions of a participant.
		credentials : {
   				 "username": "test_user1",
    				"password": "samtron555v"
				}

Methods used -

loads method from json module to fetch data from request body

serialize method from serializers module to serialize querysets to required formates

