from django.shortcuts import render
from django.views import View
from .forms import GrnForms, GrnDetailsForms, StockForms, StockOutForms
from .models import Grn, GrnDetails, Stock, StockOut
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
        grns = Grn.objects.all().order_by("-id")
        store = Store.objects.all().order_by("-id")
        item = Item.objects.all().order_by("-id")
        context = {'grns': grns, 'stores': store, 'items': item}
        return render(request, self.template_name, context)

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
            unit_price = payload.getlist('unit_price')
            zipped = zip(item, quantity, unit_price)
            total_price = 0
            for item, quantity, unit_price in zipped:
                data = {'grn': grn.id, 'item': item,
                        'quantity': quantity, 'unit_price': unit_price}

                grn_details = GrnDetailsForms(data)
                if grn_details.is_valid():
                    grn_details.save()

                # total price update
                total_price += int(unit_price) * int(quantity)
            grn.total_price = total_price
            grn.save()

            # update stock
            grn_details = GrnDetails.objects.filter(grn=grn.id)
            for grn_detail in grn_details:
                # if stock dont exists
                stock_query = Stock.objects.filter(item=grn_detail.item)
                if stock_query.exists():
                    stock = stock_query.last()
                    stock.quantity = stock.quantity + grn_detail.quantity
                    stock.save()
                else:
                    data = {'item': grn_detail.item.id, 'store': grn.store.id,
                            'quantity': grn_detail.quantity}
                    stock_serializer = StockForms(data)
                    if stock_serializer.is_valid():
                        stock_serializer.save()
                    else:
                        massage = stock_serializer.errors
                        messages.warning(request, massage)
                        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            massage = "grn & stock added"
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
        stocks = Stock.objects.all().order_by("-id")
        context = {"stocks": stocks}
        return render(request, self.template_name, context)


class StockDetailsView(View):
    @csrf_exempt
    def get(self, request):
        stock_id = request.GET.get('id')
        print(stock_id)
        stocks = Stock.objects.filter(id=stock_id).values()

        return JsonResponse({'stocks': list(stocks)})


class StockOutView(View):
    template_name = "stock/stock_out.html"
    form_class = StockOutForms

    def get(self, request):
        stocks = Stock.objects.all().order_by("-id")
        stock_outs = StockOut.objects.all().order_by("-id")
        context = {"stocks": stocks, "stock_outs": stock_outs}
        return render(request, self.template_name, context)

    def post(self, request):
        payload = request.POST
        stockList = payload.getlist('item')
        quantityList = payload.getlist('quantity')
        remarksList = payload.getlist('remarks')
        zipped = zip(stockList, quantityList, remarksList)
        total_price = 0
        for stock, quantity, remarks in zipped:
            data = {'stock': stock, 'quantity': quantity, 'remarks': remarks}
            stock_out_serializer = StockOutForms(data)
            if stock_out_serializer.is_valid():
                stock_out_serializer.save()
                # update stock
                stock_query = Stock.objects.filter(id=stock)
                if stock_query.exists():
                    stock = stock_query.last()
                    stock.quantity = stock.quantity - int(quantity)
                    stock.save()

            else:
                massage = stock_out_serializer.errors
                messages.warning(request, massage)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        massage = "stock out added"
        messages.success(request, massage)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
