from django import forms
from .models import ItemType, Item

class ItemTypeForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = "__all__"

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
