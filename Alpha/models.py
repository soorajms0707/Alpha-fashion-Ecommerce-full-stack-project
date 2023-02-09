from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class registrationmodel(models.Model):
    firstname=models.CharField(max_length=25)
    lastname=models.CharField(max_length=25)
    username=models.CharField(max_length=25)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    def __str__(self):
        return self.firstname

class uploadmodel(models.Model):
    name=models.CharField(max_length=20)
    price=models.IntegerField()
    description=models.CharField(max_length=50)
    image=models.ImageField(upload_to="Alpha/static")
    def __str__(self):
        return self.name

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class cartmodel(models.Model):
    cartname=models.CharField(max_length=20)
    cartprice=models.IntegerField()
    cartdescription=models.CharField(max_length=50)
    cartimage=models.ImageField(upload_to="Alpha/static/cart")
    def __str__(self):
        return self.cartname

