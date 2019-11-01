from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views import View

from .models import CustomUser, Login


# def home(request):
#     if request.method == "POST":
#         print(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']
#         user_check = Login.objects.filter(login_username=username)
#         print(user_check)
#         if user_check:
#             if user_check[0].login_password == password:
#                 return HttpResponse("Verified Successfully")
#             else:
#                 return HttpResponse("Wrong password for the given username")
#         else:
#             return HttpResponse("User doesnt exist!")
#     else:
#         return render(request, 'main/LandingPage.html')

class Home(View):

    def get(self, request):
        return render(request, 'main/LandingPage.html')

    def post(self, request):
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user_check = Login.objects.filter(login_username=username)
        print(user_check)
        if user_check:
            if user_check[0].login_password == password:
                return HttpResponse("Verified Successfully")
            else:
                return HttpResponse("Wrong password for the given username")
        else:
            return HttpResponse("User doesnt exist!")
