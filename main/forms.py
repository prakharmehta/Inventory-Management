from django.forms import ModelForm, DateInput
from .models import (
    CustomUser,
    Role,
    Login,
    Permission,
    Inventory,
    SalesAndPurchases,
    Billing
)


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = "__all__"


class LoginForm(ModelForm):
    class Meta:
        model = Login
        fields = "__all__"


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = "__all__"


class CustomDateInput(DateInput):
    input_type = 'date'


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
        widgets = {
            'last_update': CustomDateInput()
        }


class SalesAndPurchasesForm(ModelForm):
    class Meta:
        model = SalesAndPurchases
        fields = "__all__"


class BillingForm(ModelForm):
    class Meta:
        model = Billing
        fields = "__all__"
