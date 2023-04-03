from django.db import models
from item.models import Item


class Stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.item.name + "---" + self.price + "----" + self.quantity

    class Meta:
        db_table = 'stock'
