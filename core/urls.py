from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("item/", include("item.urls")),
    path("store/", include("store.urls")),
    path("grn/", include("grn.urls")),
]
