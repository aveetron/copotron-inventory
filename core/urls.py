from django.contrib import admin
from django.urls import path, include
from item.views import DashboardView
from reports.views import ReportView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("item/", include("item.urls")),
    path("store/", include("store.urls")),
    path("grn/", include("grn.urls")),
    path("", DashboardView.as_view(), name="dashboard"),
    path("reports/", ReportView.as_view(), name='reports'),
]
