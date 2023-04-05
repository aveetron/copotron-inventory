from django.db import models
from item.models import InventoryBaseModel


class Store(InventoryBaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store'
