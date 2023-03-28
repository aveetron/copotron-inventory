from django.urls import path
from . import views

urlpatterns = [
    path("", views.storeView.as_view(), name="store"),
    path("details/<int:id>/", views.StoreDetailsView.as_view(), name="store-details"),
]
