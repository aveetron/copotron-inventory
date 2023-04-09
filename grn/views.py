from django.shortcuts import render
from django.views import View
from .forms import GrnForms, GrnDetailsForms
from .models import Grn, GrnDetails
from item.models import Item
from store.models import Store


class GrnView(View):
    form_class = GrnForms
    template_name = "grn/grn.html"

    def get(self, request):
        item = Item.objects.all()
        store = Store.objects.all()
        context = {'items': item, 'stores': store}
        return render(request,  self.template_name, context)

    def post(self, request):
        payload = request.POST
        grn_serializer = GrnForms(payload)
        if grn_serializer.is_valid():
            grn = grn_serializer.save()
        else:
            pass
