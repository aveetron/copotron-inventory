from django import forms
from .models import Grn, GrnDetails


class GrnForms(forms.ModelForm):
    class Meta:
        model = Grn
        fields = "__all__"


class GrnDetailsForms(forms.ModelForm):
    class Meta:
        model = GrnDetails
        fields = "__all__"
