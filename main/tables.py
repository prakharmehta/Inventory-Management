import django_tables2 as tables

from .models import Inventory


class InventoryTable(tables.Table):
    class Meta:
        model = Inventory
