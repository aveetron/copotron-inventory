from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib import messages
from .models import Store
from .forms import StoreForm
# Create your views here.


class storeView(View):
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
