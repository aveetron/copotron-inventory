from django.contrib import admin
from django.urls import path, include
from item.views import DashboardView
from reports.views import ReportView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path("item/", include("item.urls")),
    path("store/", include("store.urls")),
    path("grn/", include("grn.urls")),
    path("", login_required(DashboardView.as_view()), name="dashboard"),
    path("reports/", login_required(ReportView.as_view()), name='reports'),
    path("users/", include("users.urls")),
]
