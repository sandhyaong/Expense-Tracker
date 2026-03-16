from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect('/login/')

def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})

from django.contrib.auth.models import User
from django.shortcuts import redirect

def add_user(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST["role"]

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.profile.role = role
        user.profile.save()

        return redirect("/users/")

    return render(request, "users/add_user.html")

# def assign_role(request, id):

#     user = User.objects.get(id=id)

#     if request.method == "POST":

#         role = request.POST["role"]

#         user.profile.role = role
#         user.profile.save()

#         return redirect("/users/")

#     return render(request,"users/assign_role.html",{"user":user})
# AssignRole
from .models import Profile

def assign_role(request, id):

    user = User.objects.get(id=id)

    # ensure profile exists
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":

        role = request.POST["role"]

        profile.role = role
        profile.save()

        return redirect("/users/")

    return render(request, "users/assign_role.html", {
        "user": user
    })

# create User
def create_user(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.profile.role = role
        user.profile.save()

        return redirect("/users/")

    return render(request,"users/create_user.html")