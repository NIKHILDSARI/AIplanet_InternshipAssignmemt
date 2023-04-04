from django.urls import path
from . import views

urlpatterns = [
    path('create_hackathon/',views.Create_hackathon, name= 'create_hackathon'),
    path('uploadsubmission/',views.Upload_Submission, name= 'uploadsubmission'),
    path('registration/',views.Registration, name= 'registration'),
    path('enrolledlist/',views.User_enrolled_hackathons, name= 'enrolledlist'),
    path('allsubmissions/',views.All_Submissions, name= 'enrolledlist'),
    path('listofhackathons/',views.Hackathon_list, name= 'listofhackathons'),
    path('clickonsubmission/',views.click_on_submission, name= 'click'),
    path('favouritesubmissions/',views.Favourite_submissions, name= 'favourite'),
    




]