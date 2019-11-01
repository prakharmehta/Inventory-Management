from django.db import models

from django.db import models
import uuid

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('O', 'Others'))
ROLES = (('B', 'Billing'), ('P', 'Purchases'), ('S', 'Sales'))


class CustomUser(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user_mobile = models.CharField(
        max_length=15)  # Need to set it as charfield because postgres has some issues with large integers
    user_address = models.CharField(max_length=50)
    user_name = models.CharField(max_length=20)
    dob = models.DateField()
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user_email = models.EmailField()


class Roles(models.Model):
    role_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    role_name = models.CharField(max_length=10,
                                 null=False)  # Null = False by default by can put it this way for sir to show all the constraints
    role_desc = models.CharField(max_length=30, null=True)


class Login(models.Model):
    login_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    login_role_id = models.CharField(max_length=20, choices=ROLES)  # Check if required to be converted to a number
    login_username = models.CharField(max_length=15)
    login_password = models.CharField(max_length=32)  # Add check for min_length in views.add


class Permission(models.Model):
    per_id = models.CharField(max_length=20)
    per_role_id = models.OneToOneField(Login,
                                       on_delete=models.CASCADE)  # Check if this field is suppose to be left blank
    per_name = models.CharField(max_length=20)
    per_module = models.CharField(max_length=20)


class Inventory(models.Model):
    item_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    item_amount = models.IntegerField()
    item_sale_cost = models.FloatField()
    item_pur_cost = models.FloatField()
    last_update = models.DateTimeField()
    item_description = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.item_id)


# Sales and Purchases can be merged
TRANSACTIONS = (('S', 'Sales'), ('P', 'Purchases'))


class SalesAndPurchases(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    type = models.CharField(max_length=1, choices=TRANSACTIONS)
    item_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    transaction_cus_id = models.CharField(max_length=15)  # Check if blank is also to be allowed
    transaction_amt = models.FloatField()
    transaction_date = models.DateField(auto_now_add=True)
    bill_produced = models.BooleanField(default=0)  # Converted this to a boolean field

    def __str__(self):
        return str(self.transaction_id)


class Billing(models.Model):
    bill_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    item_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # Put it asap - This is the Inventory table
    transaction_id = models.ForeignKey(SalesAndPurchases, on_delete=models.CASCADE)  # Need to make this also right
    bill_total = models.FloatField()
    bill_date = models.DateField(auto_now_add=True)
    bill_status = models.CharField(max_length=30, default="Pending")

    def __str__(self):
        return str(self.bill_id)



