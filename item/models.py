from django.db import models


class InventoryBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Uom(InventoryBaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "uom"


class ItemType(InventoryBaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "item_type"


class Item(InventoryBaseModel):
    item_code = models.CharField(max_length=50, null=True, blank=True)
    item_type = models.ForeignKey(
        ItemType, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    uom = models.ForeignKey(Uom, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "item"
