from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Create_hackathons(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    background_image = models.ImageField(upload_to='uploads/',blank=True)
    hackathon_image_logo = models.ImageField(upload_to='uploads/',blank=True)
    submission_type = models.CharField(max_length=200,null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    reward_prize = models.CharField(max_length=200,null=True,blank=True)
    github_repository = models.URLField(max_length=200)
    other_links = models.URLField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self) -> str:
        try:
            return  ' Hackathons : ' + self.title + ' : Reward_prize : ' + self.reward_prize + ' : Start : ' + str(self.start_date) + ' : End : ' + str(self.end_date) 
        except :
            return ' Hackathons : nulls inside' 

class Hackathon_Registeration(models.Model):
    participant = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    participant_name = models.CharField(max_length=200,null=True,blank=True)
    enrolled_hackathon = models.CharField(max_length=200,null=True,blank=True)
    date_of_registration = models.DateField(auto_now_add=True,blank=True)
    email = models.EmailField(max_length = 254,null=True,blank=True)
    date_time = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self) -> str:
        return 'Partcipant :' + self.participant_name + ' : Hackathon : ' + self.enrolled_hackathon + ' : Enrolled_on : ' + str(self.date_of_registration)
    
class Submissions(models.Model):
    participant = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    enrolled_hackathon = models.CharField(max_length=200,null=True,blank=True)
    submission_name = models.CharField(max_length=200,null=True,blank=True)
    submission_summary = models.TextField(null=True,blank=True)
    submission_as_link = models.URLField(max_length=200,blank=True,default='empty')
    submission_as_file = models.FileField(upload_to='uploads/',blank=True,default='empty')
    favourite = models.BooleanField(null=True,blank=True)
    date_of_submission = models.DateField(auto_now_add=True,blank=True)
    date_time = models.DateTimeField(auto_now_add=True,blank=True)
    submission_type = models.CharField(max_length=200,null=True,blank=True)


    def __str__(self) -> str:
        if self.submission_type == None:
            return str(self.participant) + ' : ' + self.enrolled_hackathon + ' : submission : ' + str(self.date_of_submission) 
        else:
            return str(self.participant) + ' : ' + self.enrolled_hackathon + ' : submission : ' + str(self.date_of_submission) + ' : type :' + self.submission_type


    

