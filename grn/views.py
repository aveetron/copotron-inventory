from django.shortcuts import render
from django.views import View
from .forms import GrnForms, GrnDetailsForms
from .models import Grn, GrnDetails
from item.models import Item
from store.models import Store
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect


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
            item = payload.getlist('item')
            quantity = payload.getlist('quantity')
            zipped = zip(item, quantity)
            for item, quantity in zipped:
                data = {'grn': grn.id, 'item': item, 'quantity': quantity}

                grn_details = GrnDetailsForms(data)

                if grn_details.is_valid():
                    grn_details.save()
            grn.save()
            massage = "grn created"
            messages.success(request, massage)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            massage = grn_serializer.errors
            messages.warning(request, massage)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
