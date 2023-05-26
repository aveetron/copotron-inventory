from django import forms
from users.models import BannerImage

class BannerImageForm(forms.ModelForm):
    class Meta:
        model = BannerImage
        fields = "__all__"