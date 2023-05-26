from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ItemTypeForm, ItemForm, UomForm
from django.views.generic import View
from .models import Item, ItemType, Uom
from grn.models import *
from store.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, QueryDict


class DashboardView(View):
    template_name = "dashboard/dashboard.html"

    def get(self, request):
        try:
            total_item = Item.objects.all().count()
            total_grn = Grn.objects.all().count()
            total_stock = Stock.objects.all().count()
            total_store = Store.objects.all().count()
            total_stock_out = StockOut.objects.all().count()
            context = {"total_item": total_item, "total_grn": total_grn,
                       "total_stock": total_stock, "total_store": total_store,
                       "total_stock_out": total_stock_out}
            return render(request, self.template_name, context)
        except Exception as e:
            messgae = e.args[0]
            messages.warning(request, messgae)
            return redirect('login')


class ItemTypeView(View):
    form_class = ItemTypeForm
    template_name = "item/item_type.html"
    dashboard_view = DashboardView()

    def get(self, request, *args, **kwargs):
        item_types = ItemType.objects.all().order_by("-id")
        context = {"item_types": item_types}
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            payload = request.POST
            item_type_serializer = self.form_class(payload)
            if item_type_serializer.is_valid():
                if ItemType.objects.filter(name__iexact=item_type_serializer.data["name"]):
                    message = "item type already exists"
                    messages.warning(request, message)
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

                item_type_serializer.save()
            else:
                message = item_type_serializer.errors
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            message = "item type created"
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ItemTypeDetailsView(View):
    form_class = ItemTypeForm
    template_name = "item/item_type.html"

    @csrf_exempt
    def get(self, request):
        itemType = ItemType.objects.filter(id=request.GET.get("id")).values()
        return JsonResponse({"itemType": list(itemType)})

    def post(self, request):
        try:
            payload = request.POST
            item_type = ItemType.objects.get(id=payload.get("id"))
            item_type_serializer = self.form_class(payload, instance=item_type)
            if item_type_serializer.is_valid():
                if ItemType.objects.filter(name__iexact=item_type_serializer.data["name"]).exclude(
                        id=payload.get("id")):
                    message = "item type already exists"
                    messages.warning(request, message)
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                item_type_serializer.save()
            else:
                message = item_type_serializer.errors
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            message = "item type updated"
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def delete(self, request):
        try:
            payload = QueryDict(request.body)
            item_type_id = payload.get("id")
            item_type = ItemType.objects.get(id=item_type_id)
            item_type.delete()
            return JsonResponse({'delete': True})
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ItemView(View):
    form_class = ItemForm
    template_name = "item/items.html"

    def get(self, request):
        items = Item.objects.all().order_by("-id")
        item_types = ItemType.objects.all().order_by("-id")
        uoms = Uom.objects.all().order_by("-id")
        context = {"items": items, "item_types": item_types, "uoms": uoms}
        return render(request, self.template_name, context)

    def post(self, request):
        item_data = request.POST
        item_data = request.POST.copy()
        item_code = Item.objects.all().count() + 1
        item_code = "Item-" + str(item_code).zfill(9)
        item_data['item_code'] = item_code
        item_form = self.form_class(item_data)
        if item_form.is_valid():
            item_form.save()
            message = "Item created successfully."
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            message = item_form.errors
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ItemDetailView(View):
    form_class = ItemForm
    template_name = "item/items.html"

    @csrf_exempt
    def get(self, request):
        item = Item.objects.filter(id=request.GET.get("id")).values()
        return JsonResponse({"item": list(item)})

    def post(self, request):
        try:
            payload = request.POST
            item = Item.objects.get(id=payload.get("id"))
            item_serializer = self.form_class(payload, instance=item)
            if item_serializer.is_valid():
                if Item.objects.filter(name__iexact=item_serializer.data["name"]).exclude(id=payload.get("id")):
                    message = "item already exists"
                    messages.warning(request, message)
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                item_serializer.save()
            else:
                message = item_serializer.errors
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            message = "item updated"
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    @csrf_exempt
    def delete(self, request):
        try:
            payload = QueryDict(request.body)
            item_id = payload.get("id")
            item = Item.objects.get(id=item_id)
            item.delete()
            return JsonResponse({'delete': True})
        except Exception as e:
            return JsonResponse({"delete": e.args[0]})


class UomView(View):
    from_class = UomForm
    template_name = "uom/uom.html"

    def get(self, request):
        uoms = Uom.objects.all().order_by("-id")
        context = {"uoms": uoms}
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            payload = request.POST
            uom_serializer = self.from_class(payload)
            if uom_serializer.is_valid():
                if Uom.objects.filter(name__iexact=uom_serializer.data["name"]):
                    message = "Uom already exists"
                    messages.warning(request, message)
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                uom_serializer.save()
            else:
                message = uom_serializer.errors
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            message = "Uom created"
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class UomDetailsView(View):
    form_class = UomForm
    template_name = "uom/uom.html"

    @csrf_exempt
    def get(self, request):
        uom = Uom.objects.filter(id=request.GET.get("id")).values()
        return JsonResponse({"uom": list(uom)})

    def post(self, request):
        try:
            payload = request.POST
            uom = Uom.objects.get(id=payload.get("id"))
            uom_serializer = self.form_class(payload, instance=uom)
            if uom_serializer.is_valid():
                if Uom.objects.filter(name__iexact=uom_serializer.data["name"]).exclude(id=payload.get("id")):
                    message = "Uom already exists"
                    messages.warning(request, message)
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                uom_serializer.save()
            else:
                message = uom_serializer.errors
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            message = "Uom updated"
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def delete(self, request):
        try:
            payload = QueryDict(request.body)
            uom_id = payload.get("id")
            uom = Uom.objects.get(id=uom_id)
            uom.delete()
            return JsonResponse({'delete': True})
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
