from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views import View

from .models import CustomUser, Login, SalesAndPurchases


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


class SalesAndPurchasesTablePage(View):
    def get(self, request):
        queryset = SalesAndPurchases.objects.values()
        context = {}
        for i in queryset:
            context.update({str(i['transaction_id']): i})
        #print(context)
        return render(request, 'main/SalesAndPurchases.html', {"context": context})


class Purchases(View):
    def get(self, request):
        return render(request, 'main/purchases.html')


class Sample2(View):
    def get(self, request):
        return render(request, 'main/sample2.html')


