from django.urls import path
from . import views

urlpatterns = [
    path("", views.storeView.as_view(), name="store"),
    path("edit_store", views.editStore.as_view(), name="edit_store"),
    path("update_store", views.updateStore.as_view(), name="update_store"),
    path("delete_store", views.deleteStore.as_view(), name="delete_store"),
]
