from django.db import models

# Create your models here.
from django.db import models
import re
from datetime import date

# Create your models here.

class userManager(models.Manager):
    def validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_error']="Invalid Email"
        users = User.objects.filter(email = postData['email'])
        if users:
            errors['email_format']="The email is alredy exist !"
        if len(postData['first_name'])<2:
            errors["first_name"]="The length of first name should be more than 2 characters"
        if len(postData['last_name'])<2:
            errors["last_name"]="The length of last name should be more than 2 characters"
        if len(postData['email'])<2:
            errors['email']="The length of email should be more than 2 characters"
        if len(postData['password'])<8:
            errors['password']="please enter a strong password, should be at least 8 letters!"
        if postData['password']!=postData['confirm_pw']:
            errors['confirm_pw']="The passwords is not matched"
        return errors
    
class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.TextField(unique=True)
    password=models.CharField(max_length=45)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)
    objects=userManager()

class carsManager(models.Manager):
    def validator(self,postData):
        errors={}
        if len(postData['model'])<2:
            errors["model"]="Please type the model of the car"
        if len(postData['maker'])<2:
            errors["maker"]="Please type the company made the car!"
        if len(postData['price'])<2:
            errors['price']="Enter a valid Price, Please"
        if len(postData['desc'])<10:
            errors['desc']="The length of description should be more than 10 characters"
        return errors
    
class Cars(models.Model):
    model=models.CharField(max_length=45)
    maker=models.CharField(max_length=45)
    year=models.PositiveBigIntegerField(null=False)
    price=models.PositiveIntegerField()
    desc=models.TextField()
    seller=models.ForeignKey(User,related_name="cars",on_delete=models.CASCADE)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)
    is_available=models.BooleanField(default=True)
    objects=carsManager()

class Purchases(models.Model):
    car=models.ForeignKey(Cars,related_name="purchases",on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,related_name="purchases",on_delete=models.CASCADE)
    price=models.PositiveBigIntegerField(null=True)
    action=models.CharField(max_length=45,default="Processing")
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)