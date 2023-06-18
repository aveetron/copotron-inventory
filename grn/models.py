from django.db import models

from item.models import InventoryBaseModel, Item
from store.models import Store


class Grn(InventoryBaseModel):
    code = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     return self.code

    class Meta:
        db_table = "grn"


class GrnDetails(InventoryBaseModel):
    grn = models.ForeignKey(Grn, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=True, blank=True, related_name="grn_item"
    )
    quantity = models.PositiveIntegerField(null=True, blank=True)
    unit_price = models.PositiveIntegerField(null=True, blank=True)

    # def __str__(self):
    #     return self.grn.code + "---" + self.item.name

    class Meta:
        db_table = "grn_details"


class Stock(InventoryBaseModel):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=True, blank=True, related_name="stock_item"
    )
    quantity = models.PositiveIntegerField(null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.item.name

    class Meta:
        db_table = "stock"


class StockOut(InventoryBaseModel):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "stock_out"
