from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ItemTypeForm, ItemForm
from django.views.generic import View
from .models import Item, ItemType
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, QueryDict

class ItemTypeView(View):
    form_class = ItemTypeForm
    template_name = "item/item_type.html"

    def get(self, request):
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

    def get(self, request, id):
        item_type = ItemType.objects.filter(id=id).last()
        if not item_type:
            message = "There is no item type!"
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        context = {"item_type": item_type}
        pass


    def put(self, request, id):
        payload = request.POST
        item_type = ItemType.objects.filter(id=id).last()
        if not item_type:
            message = "There is no item type!"
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        item_type_serializer = self.form_class(item_type, data=payload)
        if item_type_serializer.is_valid():
            message = "item type updated"
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            message = item_type_serializer.errors
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def delete(self, request, id):
        item_type = ItemType.objects.filter(id=id).last()
        if not item_type:
            message = "There is no item type!"
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        item_type.delete()
        message = "item deleted!"
        messages.success(request, message)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ItemView(View):
    form_class = ItemForm
    template_name = "item/items.html"

    def get(self, request):
        items = Item.objects.all()
        item_types = ItemType.objects.all()
        context = {"items": items, "item_types": item_types}
        return render(request, self.template_name, context)

    def post(self, request):
        item_data = request.POST
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
    template_name = "item/item_detail.html"
    @csrf_exempt
    def get(self,request):
        item = Item.objects.filter(id=request.GET.get("id")).values()
        return JsonResponse({"item": list(item)})
    def post(self,request):
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

