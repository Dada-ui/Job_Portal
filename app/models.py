from email.policy import default
from enum import unique
from random import choices
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from app.managers import UserManager
from django.db.models import Avg,Count
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={'required': "Role must be provided"})
    email = models.EmailField(unique=True, blank=False,error_messages={'unique': "A user with that email already exists.",})

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()

    
JOB_TYPE = (
    ('Full time', "Full time"),
    ('Part time', "Part time"),
    ('Internship', "Internship"),
)
EXPERIENCE = (
    ('Fresher',"Fresher"),
    ('Experience',"Experience"),
)
BENIFITS = (
    ('Work From Home',"Work From Home"),
    ('Work From Office',"Work From Office"),
    ('Remote Job',"Remote Job"),
    ('On-site Job',"On-site Job"),
    ('Hybrid Job',"Hybird Job"),
)

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    Experience = models.CharField(choices=EXPERIENCE, max_length=20)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    package = models.IntegerField()
    benefits = models.CharField(choices=BENIFITS, max_length=50)
    job_type = models.CharField(choices=JOB_TYPE, max_length=10)
    qualifications = models.CharField(max_length=100)
    description = models.TextField()
    last_date = models.DateTimeField()
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    @staticmethod
    def all_jobs():
        return Job.objects.all()
    
    
class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
     
    def __str__(self):
        return self.email
    
    
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=254)
    resume = models.FileField(upload_to='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile_photo = models.ImageField(upload_to='')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    resume = models.FileField(upload_to='')

    def __str__(self):
        return self.user


class ProfileRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0, null=True)
    review = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)