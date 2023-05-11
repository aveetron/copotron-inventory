from django.db import models
from item.models import Item
from store.models import Store


class Grn(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'grn'


class GrnDetails(models.Model):
    grn = models.ForeignKey(
        Grn, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.grn.code + "---" + self.item.name

    class Meta:
        db_table = 'grn_details'
