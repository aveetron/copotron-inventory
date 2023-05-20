from django.urls import path
from . import views
urlpatterns = [
    path("", views.GrnView.as_view(), name="grn"),
    path("grn-details/", views.GrnDetailView.as_view(), name="grn-details"),
]
