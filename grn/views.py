from django.shortcuts import render
from django.views import View
from .forms import GrnForms, GrnDetailsForms, StockForms
from .models import Grn, GrnDetails, Stock
from item.models import Item
from store.models import Store
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class GrnView(View):
    form_class = GrnForms
    template_name = "grn/grn.html"

    def get(self, request):
        grns = Grn.objects.all()
        store = Store.objects.all()
        item = Item.objects.all()
        context = {'grns': grns, 'stores': store, 'items': item}
        return render(request,  self.template_name, context)

    def post(self, request):
        payload = request.POST
        grn_serializer = GrnForms(payload)
        if grn_serializer.is_valid():
            # auto generate grn code format: GRN-0001
            grn_code = Grn.objects.all().count() + 1
            grn_code = "GRN-" + str(grn_code).zfill(4)
            # add grn code to payload
            # save

            grn = grn_serializer.save()
            grn.code = grn_code
            item = payload.getlist('item')
            quantity = payload.getlist('quantity')
            price = payload.getlist('price')
            zipped = zip(item, quantity, price)
            for item, quantity, price in zipped:
                data = {'grn': grn.id, 'item': item,
                        'quantity': quantity, 'price': price}

                grn_details = GrnDetailsForms(data)

                if grn_details.is_valid():
                    grn_details.save()
            # calculate total price aggregate
            total_price = GrnDetails.objects.filter(
                grn=grn.id).aggregate(Sum('price'))
            grn.total_price = total_price['price__sum']
            grn.save()
            # update stock
            grn_details = GrnDetails.objects.filter(grn=grn.id)
            for grn_detail in grn_details:
                stock_serializer = StockForms()
                data = {'item': grn_detail.item.id, 'store': grn.store.id,
                        'quantity': grn_detail.quantity, 'price': grn_detail.price}
                stock_serializer = StockForms(data)
                if stock_serializer.is_valid():
                    stock_serializer.save()
                else:
                    massage = stock_serializer.errors
                    messages.warning(request, massage)
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            massage = "grn created"
            messages.success(request, massage)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            massage = grn_serializer.errors
            messages.warning(request, massage)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class GrnDetailView(View):

    @csrf_exempt
    def get(self, request):
        grn_id = request.GET.get('id')
        grn = Grn.objects.filter(id=request.GET.get("id")).values()
        storeName = Store.objects.filter(id=grn[0]['store_id']).values()

        grn_details = GrnDetails.objects.filter(grn=grn_id).values()
        for grn_detail in grn_details:
            itemName = Item.objects.filter(
                id=grn_detail['item_id']).values()
            grn_detail['item_id'] = itemName[0]['name']
        return JsonResponse({'grn': list(grn), "grn_details": list(grn_details), "storeName": list(storeName)})


class StockView(View):
    template_name = "stock/stock.html"

    def get(self, request):
        stocks = Stock.objects.all()
        context = {"stocks": stocks}
        return render(request, self.template_name, context)

