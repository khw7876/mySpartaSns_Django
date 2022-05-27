from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else :
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':
        return render(request, 'tweet/home.html')
