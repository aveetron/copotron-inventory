from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store"),
    path("details", views.StoreDetailsView.as_view(), name="store-details"),
]
