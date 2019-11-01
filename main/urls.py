from django.urls import path
from . import  views
urlpatterns = [
    path('', views.Home.as_view()),
    path('sample/', views.SalesAndPurchasesTablePage.as_view()),
    path('purchases/', views.Purchases.as_view()),
    path('sample2/', views.Sample2.as_view()),
]
