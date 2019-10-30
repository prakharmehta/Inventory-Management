from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import CustomUser

def home(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user_check = CustomUser.objects.filter(username=username)
        print(user_check)
        if user_check:
            if user_check[0].password == password:
                return HttpResponse("Verified Successfully")
            else:
                return HttpResponse("Wrong password for the given username")
        else:
            return HttpResponse("User doesnt exist!")
    else:
        return render(request,'products/LandingPage.html')