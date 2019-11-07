from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
urlpatterns = [
    path('', views.Home.as_view()),
    path('sample/', csrf_exempt(views.SalesAndPurchasesTablePage.as_view())),
    #path('purchases/', views.Purchases.as_view()),
    path('sample2/', csrf_exempt(views.Sample2.as_view())),
    path('sample3/', csrf_exempt(views.Sample3.as_view())),
    path('billing/', csrf_exempt(views.BillingView.as_view())),
    path('inventory/', csrf_exempt(views.InventoryEditByAdmin.as_view())),
    path('inventoryTable/', csrf_exempt(views.InventoryTableView.as_view())),
    path('billingTable/', views.BillingTableView.as_view()),
    path('employee/', csrf_exempt(views.EmployeeAddView.as_view())),
    path('employeeTable/', csrf_exempt(views.EmployeeTableView.as_view())),
    path('adminPage/', views.SuperAdminPage.as_view()),
    path('billingTableForAdmin/', views.BillingTableViewForAdmin.as_view()),
]
