from django.shortcuts import render
from django.views import View
from .forms import GrnForms, GrnDetailsForms
from .models import Grn, GrnDetails


class GrnView(View):
    form_class = GrnForms
    template_name = "grn/grn.html"

    def get(self, request):
        # grn = Grn.objects.all().order_by("-id")
        # context = {"grn": grn}
        return render(request,  self.template_name)

    def post(self, request):
        payload = request.POST
        grn_serializer = GrnForms(payload)
        if grn_serializer.is_valid():
            grn = grn_serializer.save()
        else:
            pass
