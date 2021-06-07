from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    if "user_id" in request.session:
        user_info = Users.objects.get(id = request.session["user_id"])
        all_prods = Products.objects.all()
        context = {
            "user_info" : user_info,
            "all_prods" : all_prods
        }
        return render(request, 'ecommerce_app/index.html', context)
    else:
        return render(request, 'ecommerce_app/index.html')

def admin_page(request, location):
    if "user_id" in request.session:
        user = Users.objects.get(id = request.session["user_id"])
        if user.level == 0:
            context = {
                "user_info" : user
            }
            if location == "product":
                return render(request, 'ecommerce_app/admin_product_page.html', context)
            if location == "orders":
                return render(request, 'ecommerce_app/admin_orders_page.html', context)
        return redirect("/")
    return redirect("/")

def account_page(request, user_id, location):
    if "user_id" in request.session:
        if request.session["user_id"] != int(user_id):
            return redirect(f"/account/{request.session['user_id']}/{location}")
        user_info = Users.objects.get(id = user_id)
        context = {
            "user_info" : user_info
        }
        if location == "info":
            return render(request, 'ecommerce_app/account_info_page.html', context)
        if location == "orders":
            return render(request, 'ecommerce_app/account_orders_page.html', context)
    return redirect("/")

def edit_info_page(request, user_id, info):
    if "user_id" in request.session:
        if request.session["user_id"] != int(user_id):
            return redirect(f"/account/{request.session['user_id']}/{name}")
        user_info = Users.objects.get(id = user_id)
        context = {
            "user_info" : user_info
        }
        if info == "name":
            return render(request, 'ecommerce_app/edit_name.html', context)
        if info == "email":
            return render(request, 'ecommerce_app/edit_email.html', context)
        if info == "password":
            return render(request, 'ecommerce_app/edit_password.html', context)
    return redirect("/")

def process_edit(request, user_id):
    if request.method == "POST":
        user = Users.objects.get(id = user_id)

        # validating name on edit
        if request.POST["edit_info"] == "name":
            errors = Users.objects.update_name_validator(request.POST)
            if len(errors) > 0:
                for key,value in errors.items():
                    messages.error(request, value, extra_tags=f"{key}")
                return redirect(f"/account/{user_id}/name/edit")
            isFirst = True
            for i in range(len(request.POST["name"])):
                if i == len(request.POST["name"])-1:
                    fname = request.POST["name"]
                    lname = ""
                    break
                if request.POST["name"][i] != " ":
                    continue
                if request.POST["name"][i] == " ":
                    if isFirst:
                        fname = request.POST["name"][:i]
                        print(fname)
                        isFirst = False
                    if not request.POST["name"][i+1] == " ":
                        lname = request.POST["name"][i+1:]
                        print(lname)
                        break
                    continue
            fname = fname.lower()
            lname = lname.lower()
            user.first_name = fname.capitalize()
            user.last_name = lname.capitalize()
            user.save()
            messages.success(request, "You have successfully modified your account!", extra_tags = "edit")
            return redirect(f"/account/{user_id}/info")

        # validating email on edit
        if request.POST["edit_info"] == "email":
            errors = Users.objects.update_email_validator(request.POST)
            check_email = Users.objects.exclude(email = user.email).filter(email = request.POST["email"])
            if len(check_email) == 1:
                messages.error(request, "Email already exists", extra_tags = "existemail")
                return redirect(f"/account/{user_id}/email/edit")
            if len(errors) > 0:
                for key,value in errors.items():
                    messages.error(request, value, extra_tags=f"{key}")
                return redirect(f"/account/{user_id}/email/edit")
            else:
                user.email = request.POST["email"]
                user.save()
                messages.success(request, "You have successfully modified your account!", extra_tags = "edit")
                return redirect(f"/account/{user_id}/info")

        # validating password on edit
        if request.POST["edit_info"] == "password":
            errors = Users.objects.update_password_validator(request.POST)
            if len(errors) > 0:
                for key,value in errors.items():
                    messages.error(request, value, extra_tags = f"{key}")
                return redirect(f"/account/{user_id}/password/edit")
            if not bcrypt.checkpw(request.POST["currentpassword"].encode(), user.password.encode()):
                messages.error(request, "Your password was incorrect. Please try again.", extra_tags = "wrongpassword")
                return redirect(f"/account/{user_id}/password/edit")
            if bcrypt.checkpw(request.POST["currentpassword"].encode(), user.password.encode()):
                pwhash = bcrypt.hashpw(request.POST["newpassword"].encode(), bcrypt.gensalt())
                user.password = pwhash.decode()
                user.save()
                messages.success(request, "You have successfully modified your account!", extra_tags = "edit")
                return redirect(f"/account/{user_id}/info")
        return redirect(f"/account/{user_id}/info")
                
            

def process_product(request):
    if request.method == "POST":
        errors = Products.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags = f"{key}")
            return redirect("/admin")
        stringprice = request.POST["pricedollar"] + "." + request.POST["pricecents"]
        totalprice = float(stringprice)
        product = Products.objects.create(name = request.POST["name"].capitalize(), image = request.FILES["image"], price = totalprice, color = request.POST["color"].lower(), gender = request.POST["gender"], clothes_type = request.POST["clothes_type"], description = request.POST["description"])
        request.session["product_id"] = product.id
        return redirect('/success')

def success_page(request):
    if "user_id" in request.session:
        if "product_id" in request.session:
            user = Users.objects.get(id = request.session["user_id"])
            if user.level == 0:
                product_info = Products.objects.get(id = request.session["product_id"])
                context = {
                    "thisprod" : product_info
                }
                return render(request, 'ecommerce_app/success_page.html', context)
        return redirect("/")
    return redirect("/")

def confirm_product(request):
    if "product_id" in request.session:
        del request.session["product_id"]
        return redirect("/admin/product")

def delete_product(request, prod_id):
    delete_product = Products.objects.get(id = prod_id)
    delete_product.delete()
    del request.session["product_id"]
    return redirect("/admin/product")


def login_page(request):
    if "user_id" in request.session:
        return redirect("/")
    return render(request, 'ecommerce_app/login.html')

def register_page(request):
    if "user_id" in request.session:
        return redirect("/")
    return render(request, 'ecommerce_app/register.html')

def process_user(request):
    if request.method == "POST":
        # Handle registration
        if request.POST["which_form"] == "register":
            errors = Users.objects.basic_validator(request.POST)
            if len(errors) > 0:
                for key,value in errors.items():
                    messages.error(request, value, extra_tags=f"{key}")
                return redirect("/register")
            # Cleaning user data to find First and Last names
            isFirst = True
            for i in range(len(request.POST["name"])):
                if i == len(request.POST["name"])-1:
                    fname = request.POST["name"]
                    lname = ""
                    break
                if request.POST["name"][i] != " ":
                    continue
                if request.POST["name"][i] == " ":
                    if isFirst:
                        fname = request.POST["name"][:i]
                        print(fname)
                        isFirst = False
                    if not request.POST["name"][i+1] == " ":
                        lname = request.POST["name"][i+1:]
                        print(lname)
                        break
                    continue
            fname = fname.lower()
            lname = lname.lower()
            pwhash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            user = Users.objects.create(first_name = fname.capitalize(), last_name = lname.capitalize(), email = request.POST["email"].lower(), password = pwhash.decode())
            request.session["user_id"] = user.id
            return redirect("/")

        # Handle Login
        if request.POST["which_form"] == "login":
            if len(request.POST["email"]) < 1 or len(request.POST["password"]) < 1:
                messages.error(request, "Enter your login information", extra_tags = "nologin")
                return redirect("/login")
            else:
                userobj = Users.objects.filter(email = request.POST["email"].lower())
                if len(userobj) == 1:
                    user = userobj[0]
                    print(user)
                    if bcrypt.checkpw(request.POST["password"].encode(), user.password.encode()):
                        request.session["user_id"] = user.id
                        return redirect("/")
                    else:
                        messages.error(request, "You could not be logged in", extra_tags = "login")
                        return redirect("/login")
                else:
                    messages.error(request, "You could not be logged in", extra_tags = "login")
                    return redirect("/login")

def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        return redirect("/")
    return redirect("/")