from django import forms

from .models import Item, ItemType, Uom


class ItemTypeForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = "__all__"


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"


class UomForm(forms.ModelForm):
    class Meta:
        model = Uom
        fields = "__all__"
