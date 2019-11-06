import datetime
import random
import string

import django
from django.db import models
import uuid

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('O', 'Others'))
ROLES = (('B', 'Billing'), ('P', 'Purchases'), ('S', 'Sales'))
# Sales and Purchases can be merged - Done
TRANSACTIONS = (('S', 'Sales'), ('P', 'Purchases'))


def random_string(length=8):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class CustomUser(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True, default=random_string(10), blank=False)
    user_name = models.CharField(max_length=20)
    user_mobile = models.CharField(max_length=15)
    dob = models.DateField()
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user_email = models.EmailField()
    user_address = models.CharField(max_length=50)


class Role(models.Model):
    role_id = models.CharField(max_length=10, primary_key=True, default=random_string(10), blank=False)
    role_name = models.CharField(max_length=10,
                                 null=False)
    role_desc = models.CharField(max_length=30, null=True)

    class Meta:
        verbose_name_plural = "Roles"


class Login(models.Model):
    login_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=random_string(10), blank=False)
    login_role_id = models.CharField(max_length=20, choices=ROLES)
    login_username = models.CharField(max_length=15)
    login_password = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Login"


class Permission(models.Model):
    per_id = models.CharField(max_length=20)
    per_role_id = models.OneToOneField(Login,
                                       on_delete=models.CASCADE)
    per_name = models.CharField(max_length=20)
    per_module = models.CharField(max_length=20)


class Inventory(models.Model):
    item_id = models.CharField(max_length=10, primary_key=True, default=random_string(10), blank=False)
    item_amount = models.IntegerField()
    item_sale_cost = models.FloatField()
    item_pur_cost = models.FloatField()
    last_update = models.DateField()
    item_description = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.item_id)

    class Meta:
        verbose_name_plural = "Inventories"


class SalesAndPurchases(models.Model):
    transaction_id = models.CharField(max_length=10, primary_key=True, default=random_string(10), blank=False)
    type = models.CharField(max_length=1, choices=TRANSACTIONS)
    item_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    transaction_cus_id = models.CharField(max_length=15)  # Check if blank is also to be allowed
    transaction_amt = models.IntegerField()
    transaction_date = models.DateField(default=django.utils.timezone.now)
    bill_produced = models.BooleanField(default=0)  # Converted this to a boolean field

    def __str__(self):
        return str(self.transaction_id)

    class Meta:
        verbose_name_plural = "Sales And Purchases"


class Billing(models.Model):
    bill_id = models.CharField(max_length=10, primary_key=True, default=random_string(10), blank=False)
    item_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    transaction_id = models.ForeignKey(SalesAndPurchases, on_delete=models.CASCADE)
    bill_total = models.FloatField()
    bill_date = models.DateField(auto_now_add=True)
    bill_status = models.CharField(max_length=30, null=True)

    def __str__(self):
        return str(self.bill_id)

    class Meta:
        verbose_name_plural = "Billings"

