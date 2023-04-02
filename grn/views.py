from django.shortcuts import render
from django.views import View
from .forms import GrnForms, GrnDetailsForms
from .models import Grn, GrnDetails

class GRNView(View):
    form_class = GrnForms
    template_name = "grn.html"

    def get(self, request):
        grn = Grn.objects.all().order_by("-id")
        context = {"grn": grn}
        return render(request, context, self.template_name)
