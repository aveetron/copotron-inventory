from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib import messages
from .models import Store
from .forms import StoreForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, QueryDict

class StoreView(View):
    form_class = StoreForm
    template_name = "store.html"

    def get(self, request):
        stores = Store.objects.all().order_by("-id")
        context = {"stores": stores}
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            payload = request.POST
            store_serializer = self.form_class(payload)
            if store_serializer.is_valid():
                if Store.objects.filter(name__iexact=store_serializer.data["name"]):
                    message = "store already exists"
                    messages.warning(request, message)
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                store_serializer.save()
            else:
                message = store_serializer.errors
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            message = "store created"
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class StoreDetailsView(View):
    form_class = StoreForm
    template_name = "store.html"

    @csrf_exempt
    def get(self, request):
        store = Store.objects.filter(id=request.GET.get("id")).values()
        return JsonResponse({'store': list(store)})

    def post(self, request):
        try:
            payload = request.POST
            store = Store.objects.get(id=payload.get("id"))
            store_serializer = self.form_class(payload, instance=store)
            if store_serializer.is_valid():
                if Store.objects.filter(name__iexact=store_serializer.data["name"]).exclude(id=payload.get("id")):
                    message = "store already exists"
                    messages.warning(request, message)
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                store_serializer.save()
            else:
                message = store_serializer.errors
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            message = "store updated"
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            message = e.args[0]
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    @csrf_exempt
    def delete(self, request):
        payload = QueryDict(request.body)
        store_id = payload.get("id")
        print(store_id)
        store = Store.objects.get(id=store_id)
        store.delete()
        return JsonResponse({'delete': True})