from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages
from django.urls import reverse
import bcrypt
from .models import User, Message, Comment
from django.db.models import Q
# Create your views here.
#render index Page
def index(request):
    if('id' in request.session):
        return redirect(reverse('wall:my_success'))
    return render(request,"wall/index.html")
#register a new user
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, key)
        # redirect the user back to the form to fix the errors
        return redirect('wall:my_home')
    #if not redirected then we create new user with hashed password.
    hash1=  bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
    newUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                 email = request.POST['email'], password= hash1.decode('utf-8'))
    messages.success(request, "Users succesfully created!")
    print(newUser.first_name)
    request.session['id'] = newUser.id
    return redirect(reverse('wall:my_success'))

#log into user
def login(request):
    if request.method == "POST":
        #checks if there is a user with email.
        loginUser = User.objects.filter(email=request.POST['email'])
        if not loginUser:
            messages.error(request, "Failed to login",'login')
            return redirect(reverse('wall:my_home'))
        #if found compare the hash of the given password to the saved hash.
        print(loginUser.first().password)
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), loginUser.first().password.encode() ):
            request.session['id'] = loginUser.first().id
            messages.success(request, "Login Succesful!")
            return redirect(reverse('wall:my_success'))
        messages.error(request, "Failed to login",'login')
        return redirect(reverse('wall:my_home'))

def success(request):
    users = User.objects.exclude(id=request.session['id'])

    context ={
        "all_but_me" : users,
        "name" : User.objects.get(id=request.session['id']).first_name,
        "myMessages" : User.objects.get(id=request.session['id']).myMessages.all().order_by('-created_at'),
        "id" : request.session['id']
        }
    return render(request,"wall/myWall.html",context)

def newsFeed(request):
    users = User.objects.filter(~Q(id=request.session['id']))
    #messages = User.objects.get(id=request.session['id']).myMessages.all()
    context ={
        "all_but_me" : users,
        "name" : User.objects.get(id=request.session['id']).first_name,
        "myMessages" : Message.objects.all().order_by('-created_at'),
        "id" : request.session['id']
        }
    return render(request,"wall/newsFeed.html",context)


def comment(request):
    if request.method == "POST":
        Comment.objects.create(comment=request.POST['content'],updater_id=User.objects.get(id=request.session['id']),message_id=Message.objects.get(id=request.POST['msg_id']))
    
    return redirect(reverse('wall:my_home'))

def send(request):
    if request.method == "POST":
        Message.objects.create(text=request.POST['content'],sender=User.objects.get(id=request.session['id']),receiver=User.objects.get(id=request.POST['ToWho']))
    return redirect(reverse('wall:my_home'))
def clear(request):
    request.session.clear()
    return redirect(reverse('wall:my_home'))