import datetime

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views import View
from .tables import InventoryTable
from .forms import InventoryForm
from .models import CustomUser, Login, SalesAndPurchases, Inventory, Billing


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


class Purchases(View):
    def get(self, request):
        return render(request, 'main/purchases.html')

    def post(self, request):
        type = 'P'
        item_id = Inventory.objects.filter(item_id=request.POST('item_id'))
        transaction_customer_id = request.POST('pur_cus_id')
        transaction_amt = request.POST('pur_amt')
        transaction_date = request.POST('pur_date')

        try:

            SalesAndPurchases.objects.create(type=type,
                                             item_id=item_id,
                                             transaction_customer_id=transaction_customer_id,
                                             transaction_amt=transaction_amt,
                                             transaction_date=transaction_date)
        except Exception as e:
            return HttpResponse("Error in adding to db")

        # print(request.POST)
        return HttpResponse("Successfully Added !")


class Sample2(View):
    # Purchase page
    def get(self, request):
        queryset = SalesAndPurchases.objects.filter(type='P').values()
        table = {}
        for i in queryset:
            table.update({str(i['transaction_id']): i})
        return render(request, 'main/sample2.html', {"table": table})

    def post(self, request):
        queryset = SalesAndPurchases.objects.filter(type='P').values()
        table = {}
        context = {}
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

        try:

            SalesAndPurchases.objects.create(type=type,
                                             item_id=item_id[0],
                                             transaction_cus_id=transaction_customer_id,
                                             transaction_amt=transaction_amt,
                                             transaction_date=transaction_date)
        except Exception as e:
            print(e)
            context.update({"messages2": "Error in adding to the database"})
            return render(request, 'main/sample2.html', {"context": context, "table": table})

        # print(request.POST)
        context.update({"messages2": "Successfully Added to Database"})
        return render(request, 'main/sample2.html', {"context": context, "table": table})


class Sample3(View):

    # Sales VIew
    def get(self, request):
        return render(request, 'main/Sales_Sample.html')

    def post(self, request):
        type = 'S'

        print(request.POST)
        item_id = Inventory.objects.filter(item_id=request.POST['item_id'])
        if not item_id:
            return HttpResponse("No good by this item id exists in the inventory")
        # In case items are not in db, and user mistakenly puts an invalid item id

        transaction_customer_id = request.POST['pur_cus_id']
        transaction_amt = request.POST['pur_amt']
        transaction_date = request.POST['pur_date']

        try:
            check = float(transaction_amt)
        except ValueError as e:
            print("Referenced")
            context = {"messages1": e}
            return render(request, 'main/Sales_Sample.html', {"context": context})

        try:

            SalesAndPurchases.objects.create(type=type,
                                             item_id=item_id[0],
                                             transaction_cus_id=transaction_customer_id,
                                             transaction_amt=transaction_amt,
                                             transaction_date=transaction_date)
        except Exception as e:
            print(e)
            context = {"messages1": e}
            return render(request, 'main/Sales_Sample.html', {"context": context})

        # print(request.POST)
        return HttpResponse("Successfully Added !")


class BillingView(View):
    transaction_id = ''
    item_id = ''
    date = ''
    choice = 'Rejected'
    bill_id = ''

    def get(self, request):
        return render(request, "main/Billing_Sample.html")

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
        return inventory_object.item_pur_cost * sales_and_purchase_object.transaction_amt

    def post(self, request):
        # Making checks to make sure user enters all fields
        check = self.params_check(request)

        context = {}
        # Check if the item id and transaction id provided exist in the database

        try:
            sales_and_purchase_object = SalesAndPurchases.objects.get(transaction_id=self.transaction_id)
        except Exception as e1:
            context.update({"messages1": "Err: {}".format(e1)})
        try:
            inventory_object = Inventory.objects.get(item_id=self.item_id)
        except Exception as e2:
            context.update({"messages2": "Err: {}".format(e2)})

        if context:
            print(context)
            return render(request, 'main/Billing_Sample.html', {"context": context})

        if Billing.objects.filter(transaction_id=sales_and_purchase_object):
            context.update({"messages1": "Err: {}".format("Cannot generate duplicate bills.")})
            return render(request, 'main/Billing_Sample.html', {"context": context})

        sales_and_purchase_instance = inventory_object.item_id
        print("Instance has ", len(str(sales_and_purchase_instance)))
        print("Actual has ", len(sales_and_purchase_object.item_id.item_id))
        if sales_and_purchase_instance != sales_and_purchase_object.item_id.item_id:
            context.update({"messages1": "Given Item Id is not related to the Transaction specified"})
            return render(request, 'main/Billing_Sample.html', {"context": context})

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
                return render(request, 'main/Billing_Sample.html', {"context": context})
            else:
                Billing.objects.create(bill_id=self.bill_id, item_id=inventory_object,
                                       transaction_id=sales_and_purchase_object,
                                       bill_total=bill_total,
                                       bill_status="Rejected")
                context.update({"messages1": "Bill Generated for Rejected Purchase object and Inventory updated"})
                return render(request, 'main/Billing_Sample.html', {"context": context})

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
                elif self.choice == 'Rejected':

                    Billing.objects.create(bill_id=self.bill_id, item_id=inventory_object,
                                           transaction_id=sales_and_purchase_object,
                                           bill_total=bill_total,
                                           bill_status="Rejected(User Rejected)")
                    context.update({"messages1": "Successfully Created Bill(User Rejected)"})
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
            except Exception as e:
                context.update({"messages1": e})

            return render(request, 'main/Billing_Sample.html', {"context": context})


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
        table = InventoryTable(Inventory.objects.all())
        return render(request, "main/Inventory_Table.html", {"table": table})


class BillingTableView(View):
    def get(self, request):
        pass







