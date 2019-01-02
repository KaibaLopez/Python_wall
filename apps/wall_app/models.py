# Inside your app's models.py file
from __future__ import unicode_literals
from django.db import models
# Create your models here.
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class RegistrationManager(models.Manager):
    def basic_validator(self,postData):
        errors ={}
        #names rules
        if len(postData['first_name']) < 3:
            errors["first_name"] = "Name should be more than 2 characters long!"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last Name should be more than 2 characters long!"
        
        #Password rules
        if len(postData['password']) < 8:
            errors["password"] = "Passowrd should be more than 2 characters long!"
        elif not re.search("[A-Z]", postData['password']): 
            errors["password"] = "Password must have at least 1 uppercase letter"
        elif not re.search("[0-9]", postData['password']): 
            errors["password"] = "Password must have at least 1 number"
        elif re.search("\s",  postData['password']):
            errors["password"] = "Password must have no empty spaces"
        elif postData['password'] != postData['confirm_password']:
            errors["password"] = "Passwords don't match"
        #email rules
        if len(postData['email']) < 1:
            errors["email"] = ("Email cannot be blank!")
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = ("Invalid Email Address!")

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    # *************************
    # Connect an instance of BlogManager to our Blog model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = RegistrationManager()
    # *************************

class Message(models.Model):
    text = models.TextField(max_length=1000)
    sender = models.ForeignKey(User, related_name="sentMessages", on_delete=models.CASCADE , null = True)
    receiver = models.ForeignKey(User, related_name="myMessages", on_delete=models.CASCADE , null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    updater_id = models.ForeignKey(User, related_name="comment", on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, related_name="comment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)