from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
urlpatterns = [
    path('', views.Home.as_view()),
    path('sample/', views.SalesAndPurchasesTablePage.as_view()),
    path('purchases/', views.Purchases.as_view()),
    path('sample2/', views.Sample2.as_view()),
    path('sample3/', views.Sample3.as_view()),
    path('billing/', csrf_exempt(views.BillingView.as_view())),
    path('inventory/', csrf_exempt(views.InventoryEditByAdmin.as_view())),
    path('inventoryTable/', views.InventoryTableView.as_view()),
]
