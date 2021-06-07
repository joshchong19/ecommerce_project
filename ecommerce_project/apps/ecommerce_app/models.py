from __future__ import unicode_literals
from django.db import models
import re

class UsersManager(models.Manager):
    def basic_validator(self,postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData["name"]) == 0:
            errors["noname"] = "Enter your name"
        if len(postData["email"]) == 0:
            errors["noemail"] = "Enter your email"
        if len(postData["email"]) >= 1 and not EMAIL_REGEX.match(postData["email"]):
            errors["invalidemail"] = "Enter a valid emaill address"
        check_email = Users.objects.filter(email = postData["email"])
        if len(check_email) == 1:
            errors["existemail"] = "Email already exists"
        if len(postData["password"]) < 6:
            errors["shortpw"] = "Password must be at least 6 characters"
        if postData["password"] != postData["confirmpw"]:
            errors["pwnotmatch"] = "Passwords must match"
        return errors

    def update_name_validator(self, postData):
        errors = {}
        if len(postData["name"]) == 0:
            errors["noname"] = "Enter your name"
        return errors

    def update_email_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData["email"]) == 0:
            errors["noemail"] = "Enter your email"
        if len(postData["email"]) >= 1 and not EMAIL_REGEX.match(postData["email"]):
            errors["invalidemail"] = "Enter a valid emaill address"
        return errors
    
    def update_password_validator(self, postData):
        errors = {}
        if len(postData["currentpassword"]) == 0:
            errors["emptyfield"] = "Enter your password"
        if len(postData["newpassword"]) < 6:
            errors["shortpw"] = "Password must be at least 6 characters"
        if postData["newpassword"] != postData["newpasswordconfirm"]:
            errors["nomatchpassword"] = "Passwords must match"
        return errors

class ProductsManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["name"]) == 0:
            errors["noname"] = "Enter product name"
        if len(postData["pricedollar"]) == 0 and len(postData["pricecents"]) == 0:
            errors["noprice"] = "Enter product price"
        if len(postData["description"]) == 0:
            errors["nodescription"] = "Enter product description"
        if len(postData["description"]) > 0 and len(postData["description"]) < 10:
            errors["shortdescription"] = "Description must be at least 10 characters"
        if len(postData["color"]) == 0:
            errors["nocolor"] = "Enter a color"
        if len(postData["color"]) > 0 and postData["colorvalid"] != "true":
            errors["invalidcolor"] = "Enter a valid color"
        if postData["filevalid"] != "true":
            errors["noimage"] = "Please select a file"
        return errors
        

class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Products(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', null = True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    color = models.CharField(max_length=45)
    gender = models.CharField(max_length=6)
    clothes_type = models.CharField(max_length=45, null = True)
    description = models.TextField()
    users_bought = models.ManyToManyField(Users,related_name='bought_products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductsManager()

class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products,related_name='part_of_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)