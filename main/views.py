import datetime

import django
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .tables import InventoryTable
from .forms import InventoryForm, CustomUserForm
from .models import CustomUser, Login, SalesAndPurchases, Inventory, Billing


class Home(View):
    """Defines the Landing Page when the home screen Loads up"""
    def get(self, request):
        return render(request, 'main/LandingPage.html')

    def post(self, request):
        print(request.POST)
        """Handling the username and password"""
        username = request.POST['username']
        password = request.POST['password']
        """First check for existence of username in login"""
        user_check = Login.objects.filter(login_username=username)
        print(user_check)
        if user_check:
            """If username exists, then check for password entered"""
            if user_check[0].login_password == password:
                role = user_check[0].login_role_id
                """Redirecting users to different pages by depending on roles"""
                """
                A- Admin
                B- Billing
                S- Sales
                P- Purchase
                """
                if role == "A":
                    return redirect("/adminPage/")
                elif role == "B":
                    return redirect("/billing/")
                elif role == "S":
                    return redirect("/sample3/")
                elif role == "P":
                    return redirect("/sample2/")
            else:
                """In case wrong password entered"""
                context = {"messages1": "Wrong set of username and password"}
                return render(request, 'main/LandingPage.html', {"context": context})

        else:
            """In case user id doesnt exist"""
            context = {"messages1": "User id does not exist"}
            return render(request, 'main/LandingPage.html', {"context": context})


class SalesAndPurchasesTablePage(View):
    def get(self, request):
        try:
            type = request.GET.get('type')
            print(type)
        except Exception as e:
            print(e)
            return HttpResponse("Wrong type sent")
        if type not in ['P', 'S', None]:
            return HttpResponse("Invalid type query")
        if not type:
            queryset = SalesAndPurchases.objects.all().values()
        else:
            queryset = SalesAndPurchases.objects.filter(type=type).values()
        context = {}
        for i in queryset:
            context.update({str(i['transaction_id']): i})
        #print(context)
        return render(request, 'main/SalesAndPurchases.html', {"context": context})

    def post(self, request):
        print(request.POST)
        return HttpResponse("Edit Page Coming Soon")


# class Purchases(View):
#     def get(self, request):
#         return render(request, 'main/purchases.html')
#
#     def post(self, request):
#         type = 'P'
#         item_id = Inventory.objects.filter(item_id=request.POST('item_id'))
#         transaction_customer_id = request.POST('pur_cus_id')
#         transaction_amt = request.POST('pur_amt')
#         transaction_date = request.POST('pur_date')
#
#         try:
#
#             SalesAndPurchases.objects.create(type=type,
#                                              item_id=item_id,
#                                              transaction_customer_id=transaction_customer_id,
#                                              transaction_amt=transaction_amt,
#                                              transaction_date=transaction_date)
#         except Exception as e:
#             return HttpResponse("Error in adding to db")
#
#         # print(request.POST)
#         return HttpResponse("Successfully Added !")


class Sample2(View):
    # Purchase page
    def get(self, request):
        queryset = SalesAndPurchases.objects.filter(type='P').values()
        table = {}
        for i in queryset:
            table.update({str(i['transaction_id']): i})
        return render(request, 'main/sample2.html', {"table": table})

    def post(self, request):
        context = {}
        table = {}
        queryset = SalesAndPurchases.objects.filter(type='P').values()
        for i in queryset:
            table.update({str(i['transaction_id']): i})
        type = 'P'
        print(request.POST)
        item_id = Inventory.objects.filter(item_id=request.POST['item_id'])
        if not item_id:
            context.update({"messages1": "No good by this item id exists in the inventory"})
            return render(request, 'main/sample2.html', {"context": context, "table": table})

        transaction_customer_id = request.POST['pur_cus_id']
        transaction_amt = request.POST['pur_amt']
        transaction_date = request.POST['pur_date']
        transaction_id = request.POST['Purchase_id']

        try:
            SalesAndPurchases.objects.get(transaction_id=transaction_id)
            context = {}
            table = {}
            queryset = SalesAndPurchases.objects.filter(type='P').values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            context.update({"messages2": "Purchase already exists"})
            return render(request, 'main/sample2.html', {"context": context, "table": table})

        except Exception as e:
            print(e)
            pass

        try:
            transaction_amt = int(transaction_amt)
        except ValueError:
            context = {}
            table = {}
            queryset = SalesAndPurchases.objects.filter(type='P').values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            context.update({"messages2": "transaction_amt is not an integer"})
            return render(request, 'main/sample2.html', {"context": context, "table": table})

        try:

            SalesAndPurchases.objects.create(transaction_id=transaction_id, type=type,
                                             item_id=item_id[0],
                                             transaction_cus_id=transaction_customer_id,
                                             transaction_amt=transaction_amt,
                                             transaction_date=transaction_date)

            table = {}
            queryset = SalesAndPurchases.objects.filter(type='P').values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            context.update({"messages2": "Successfully Added to Database"})
            return render(request, 'main/sample2.html', {"context": context, "table": table})
        except Exception as e:
            print(e)
            table = {}
            queryset = SalesAndPurchases.objects.filter(type='P').values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            context.update({"messages2": "Error in adding to the database, check date format once"})
            return render(request, 'main/sample2.html', {"context": context, "table": table})

        # print(request.POST)


class Sample3(View):

    # Sales VIew
    def get(self, request):
        context = {}
        table = {}
        queryset = SalesAndPurchases.objects.filter(type='S').values()
        for i in queryset:
            table.update({str(i['transaction_id']): i})
        return render(request, 'main/Sales_Sample.html', {"context": context, "table": table})

    def post(self, request):
        type = 'S'

        print(request.POST)
        item_id = Inventory.objects.filter(item_id=request.POST['item_id'])
        if not item_id:
            context = {}
            table = {}
            context.update({"messages1": "No good by this item id exists in the inventory"})
            queryset = SalesAndPurchases.objects.filter(type='S').values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            return render(request, 'main/Sales_Sample.html', {"context": context, "table": table})
        # In case items are not in db, and user mistakenly puts an invalid item id

        transaction_customer_id = request.POST['pur_cus_id']
        transaction_amt = request.POST['pur_amt']
        transaction_date = request.POST['pur_date']
        transaction_id = request.POST['Sales_id']

        try:
            SalesAndPurchases.objects.get(transaction_id=transaction_id)
            context = {}
            table = {}
            queryset = SalesAndPurchases.objects.filter(type='S').values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            context.update({"messages2": "Sales already exists"})
            return render(request, 'main/Sales_Sample.html', {"context": context, "table": table})

        except Exception as e:
            print(e)
            pass

        try:
            transaction_amt = int(transaction_amt)
        except ValueError:
            context = {}
            table = {}
            queryset = SalesAndPurchases.objects.filter(type='S').values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            context.update({"messages2": "transaction_amt is not an integer"})
            return render(request, 'main/Sales_Sample.html', {"context": context, "table": table})

        try:

            SalesAndPurchases.objects.create(transaction_id=transaction_id, type=type,
                                             item_id=item_id[0],
                                             transaction_cus_id=transaction_customer_id,
                                             transaction_amt=transaction_amt,
                                             transaction_date=transaction_date)
        except Exception as e:
            print(e)
            context = {}
            table = {}
            context.update({"messages1": e})
            queryset = SalesAndPurchases.objects.filter(type='S').values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            return render(request, 'main/Sales_Sample.html', {"context": context, "table": table})

        # print(request.POST)
        context = {}
        table = {}
        context.update({"messages1": "Successfully Added"})
        queryset = SalesAndPurchases.objects.filter(type='S').values()
        for i in queryset:
            table.update({str(i['transaction_id']): i})
        return render(request, 'main/Sales_Sample.html', {"context": context, "table": table})


class BillingView(View):
    transaction_id = ''
    item_id = ''
    date = ''
    choice = 'Rejected'
    bill_id = ''

    def get(self, request):
        table = {}
        queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
        for i in queryset:
            table.update({str(i['transaction_id']): i})
        return render(request, 'main/Billing_Sample.html', {"table": table})

    def params_check(self, request):
        try:
            self.transaction_id = request.POST['trans_id']
            self.item_id = request.POST['item_id']
            self.date = request.POST['date']
            if 'choice' not in request.POST:
                self.choice = 'Accepted'

            if 'bill_id' in request.POST:
                self.bill_id = request.POST['bill_id']
            print(request.POST)

            context = {}
            if self.transaction_id == '':
                context.update({"messages1": "Database Error : Transaction ID cannot be a null field"})
            if self.item_id == '':
                context.update({"messages2": "Database Error : Item ID cannot be a null field"})
            if self.date == '':
                context.update({"messages3": "Database Error: Date cannot be a null field"})
            if self.bill_id == '':
                context.update({"messages": "Database Error: Purchase ID cannot be a null field"})
            return render(request, 'main/Billing_Sample.html', {"context": context})

        except Exception as e:
            print(e)
            context = {"messages": e}
            return render(request, 'main/Billing_Sample.html', {"context": context})

    def bill(self, inventory_object, sales_and_purchase_object):
        if sales_and_purchase_object.type == "S":
            return inventory_object.item_sale_cost * sales_and_purchase_object.transaction_amt
        else:
            return inventory_object.item_pur_cost * sales_and_purchase_object.transaction_amt

    def post(self, request):
        # Making checks to make sure user enters all fields
        check = self.params_check(request)

        context = {}

        try:
            Billing.objects.get(bill_id=self.bill_id)
            context = {}
            table = {}
            queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            context.update({"messages2": "Billing already exists"})
            return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})

        except Exception as e:
            print(e)
            pass

        try:
            sales_and_purchase_object = SalesAndPurchases.objects.get(transaction_id=self.transaction_id)
            if self.date > str(django.utils.timezone.now().date()):
                context.update({"messages1": "Enter valid date"})
        except Exception as e1:
            context.update({"messages1": "Err: {}".format(e1)})

        try:
            inventory_object = Inventory.objects.get(item_id=self.item_id)
        except Exception as e2:
            context.update({"messages2": "Err: {}".format(e2)})

        if context:
            print(context)
            table = {}
            queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})

        if Billing.objects.filter(transaction_id=sales_and_purchase_object):
            context.update({"messages1": "Err: {}".format("Cannot generate duplicate bills.")})
            table = {}
            queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})

        sales_and_purchase_instance = inventory_object.item_id
        print("Instance has ", len(str(sales_and_purchase_instance)))
        print("Actual has ", len(sales_and_purchase_object.item_id.item_id))
        if sales_and_purchase_instance != sales_and_purchase_object.item_id.item_id:
            context.update({"messages1": "Given Item Id is not related to the Transaction specified"})
            table = {}
            queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
            for i in queryset:
                table.update({str(i['transaction_id']): i})
            return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})

        type = sales_and_purchase_object.type
        context = {}

        bill_total = self.bill(inventory_object, sales_and_purchase_object)
        if type == 'P':
            if self.choice == "Accepted":
                Billing.objects.create(
                    bill_id=self.bill_id,
                    item_id=inventory_object,
                    transaction_id=sales_and_purchase_object,
                    bill_total=bill_total,
                    bill_status="Accepted")

                Inventory.objects.filter(
                    item_id=inventory_object.item_id
                ).update(
                    item_amount=inventory_object.item_amount+sales_and_purchase_object.transaction_amt,
                    last_update=datetime.datetime.now().date()
                )

                SalesAndPurchases.objects.filter(
                    transaction_id=sales_and_purchase_object.transaction_id,
                ).update(
                    bill_produced=1
                )
                context.update({"messages1": "Bill Generated for Purchase object and Inventory updated"})
                table = {}
                queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
                for i in queryset:
                    table.update({str(i['transaction_id']): i})
                return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})
            else:

                Billing.objects.create(bill_id=self.bill_id, item_id=inventory_object,
                                       transaction_id=sales_and_purchase_object,
                                       bill_total=bill_total,
                                       bill_status="Rejected(User Rejected)")
                context.update({"messages1": "Bill Generated for Rejected Purchase object"})
                table = {}
                queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
                for i in queryset:
                    table.update({str(i['transaction_id']): i})
                return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})

        elif type == 'S':

            try:
                if inventory_object.item_amount < sales_and_purchase_object.transaction_amt:
                    print("Inventory Amount is ", inventory_object.item_amount)
                    print("Sales or Purchase object is ", sales_and_purchase_object.transaction_amt)
                    context.update({"messages1": "No of items to be sold cannot be greater than the amount in inventory"})
                    Billing.objects.create(bill_id=self.bill_id, item_id=inventory_object,
                                           transaction_id=sales_and_purchase_object,
                                           bill_total=bill_total,
                                           bill_status="Rejected(Over demand)")

                    SalesAndPurchases.objects.filter(
                        transaction_id=sales_and_purchase_object.transaction_id,
                    ).update(
                        bill_produced=1
                    )
                    context.update({"messages1": "Successfully Created Bill(Over Demand)"})
                    table = {}
                    queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
                    for i in queryset:
                        table.update({str(i['transaction_id']): i})
                    return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})
                elif self.choice == 'Rejected':

                    Billing.objects.create(bill_id=self.bill_id, item_id=inventory_object,
                                           transaction_id=sales_and_purchase_object,
                                           bill_total=bill_total,
                                           bill_status="Rejected(User Rejected)")

                    SalesAndPurchases.objects.filter(
                        transaction_id=sales_and_purchase_object.transaction_id,
                    ).update(
                        bill_produced=1
                    )
                    context.update({"messages1": "Successfully Created Bill(User Rejected)"})
                    table = {}
                    queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
                    for i in queryset:
                        table.update({str(i['transaction_id']): i})
                    return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})
                else:

                    Billing.objects.create(bill_id=self.bill_id, item_id=inventory_object,
                                           transaction_id=sales_and_purchase_object,
                                           bill_total=bill_total,
                                           bill_status="Accepted")
                    Inventory.objects.filter(
                        item_id=inventory_object.item_id
                    ).update(
                        item_amount=inventory_object.item_amount - sales_and_purchase_object.transaction_amt,
                        last_update=datetime.datetime.now().date()
                    )

                    SalesAndPurchases.objects.filter(
                        transaction_id=sales_and_purchase_object.transaction_id,
                    ).update(
                        bill_produced=1
                    )
                    context.update({"messages1": "Successfully Created Bill with Accepted status"})

                    table = {}
                    queryset = SalesAndPurchases.objects.filter(bill_produced=0).values()
                    for i in queryset:
                        table.update({str(i['transaction_id']): i})
                    return render(request, 'main/Billing_Sample.html', {"context": context, "table": table})
            except Exception as e:
                context.update({"messages1": e})


class InventoryEditByAdmin(View):
    def get(self, request):
        form = InventoryForm()
        return render(request, "main/inventory.html", {"form": form})

    def post(self, request):
        form = InventoryForm(request.POST)

        if form.is_valid():
            form.save()
            context = {}
            context.update({"messages1": "Successfully saved item"})
            return render(request, "main/inventory.html", {"form": form, "context": context})

        else:
            return render_to_response("main/inventory.html", {"form": form})


class InventoryTableView(View):
    def get(self, request):
        queryset = Inventory.objects.all().values()
        table = {}
        for i in queryset:
            table.update({str(i['item_id']): i})
        print(table)
        return render(request, 'main/Inventory_Table.html', {"table": table})

    def post(self, request):
        item_id = request.POST['primary_key']
        inventory_instance = Inventory.objects.all()
        garbage_object = inventory_instance.filter(item_id=item_id)
        context = {}
        table = {}
        inventory_instance_values = inventory_instance.values()
        for i in inventory_instance_values:
            table.update({str(i['item_id']): i})
        print(context)
        if garbage_object:
            garbage_object.delete()
            inventory_instance = Inventory.objects.all()
            inventory_instance_values = inventory_instance.values()
            context = {}
            table = {}
            for i in inventory_instance_values:
                table.update({str(i['item_id']): i})
            context.update({"messages1": "Successfully Deleted!"})
            return render(request, "main/Inventory_Table.html", {"table": table, "context": context})
        else:
            inventory_instance = Inventory.objects.all()
            inventory_instance_values = inventory_instance.values()
            context = {}
            table = {}
            for i in inventory_instance_values:
                table.update({str(i['item_id']): i})
            context.update({"messages1": "Already deleted!"})
            return render(request, "main/Inventory_Table.html", {"table": table, "context": context})


class BillingTableView(View):
    def get(self, request):
        queryset = Billing.objects.all().values()
        context = {}
        for i in queryset:
            context.update({str(i['bill_id']): i})
        print(context)
        return render(request, 'main/Billing_Table_View.html', {"context": context})


class EmployeeAddView(View):

    def get(self, request):
        form = CustomUserForm()
        return render(request, "main/employee.html", {"form": form})

    def post(self, request):
        form = CustomUserForm(request.POST)

        if form.is_valid():
            form.save()
            context = {}
            context.update({"messages1": "Successfully saved user details"})
            return render(request, "main/employee.html", {"form": form, "context": context})

        else:
            return render_to_response("main/employee.html", {"form": form})


class EmployeeTableView(View):
    def get(self, request):
        queryset = CustomUser.objects.all().values()
        print(queryset)
        table = {}
        for i in queryset:
            table.update({str(i['user_id']): i})
        # print(context)
        return render(request, 'main/Employee_Table.html', {"table": table})

    def post(self, request):
        user_id = request.POST['primary_key']
        employee_instance = CustomUser.objects.all()
        garbage_object = employee_instance.filter(user_id=user_id)
        context = {}
        table = {}
        employee_instance_values = employee_instance.values()
        for i in employee_instance_values:
            table.update({str(i['user_id']): i})
        print(context)
        if garbage_object:
            garbage_object.delete()
            employee_instance = CustomUser.objects.all()
            employee_instance_values = employee_instance.values()
            table = {}
            for i in employee_instance_values:
                table.update({str(i['user_id']): i})
            context.update({"messages1": "Successfully Deleted!"})
            return render(request, "main/Employee_Table.html", {"table": table, "context": context})
        else:
            employee_instance = CustomUser.objects.all()
            employee_instance_values = employee_instance.values()
            table = {}
            for i in employee_instance_values:
                table.update({str(i['user_id']): i})
            context.update({"messages1": "Already deleted!"})
            return render(request, "main/Employee_Table.html", {"table": table, "context": context})


class SuperAdminPage(View):
    def get(self, request):
        return render(request, "main/admin_page.html")


class BillingTableViewForAdmin(View):
    def get(self, request):
        queryset = Billing.objects.all().values()
        context = {}
        for i in queryset:
            context.update({str(i['bill_id']): i})
        print(context)
        return render(request, 'main/Billing_Table_for_Admin.html', {"context": context})
