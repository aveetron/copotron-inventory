from django.contrib import admin

from .models import Grn, GrnDetails, Stock

admin.site.register(Grn)
admin.site.register(GrnDetails)
admin.site.register(Stock)
