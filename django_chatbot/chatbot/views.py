from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Chat
from django.utils import timezone
key='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'
openai.api_key=key

def askai(message):
    response=openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer=response.choices[0].text.strip()
    return answer

# Create your views here.
def chatbot(request):
    chats=Chat.objects.filter(user=request.user)
    if request.method=="POST":
        message=request.POST.get('message')
        response=askai(message)
        chat=Chat(user=request.user,message=message,response=response,created_at=timezone.now())
        chat.save()
        return JsonResponse({"message":message,"response":response})
    return render(request,'chatbot.html',{'chats':chats})

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        if password1==password2:
            try:
                user=User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message='Error Creating Account'
                return render(request,'register.html',{'error_message':error_message})
        else:
            error_message='Password did not match'
            return render(request,'register.html',{'error_message':error_message})
    return render(request,'register.html')

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if user:
            auth.login(request,user)
            return redirect('chatbot')
        else:
            error_message='Invalid username or password'
            return render(request,'login.html',{'error_message':error_message})
    else:
        return render(request,'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('login')
             




        