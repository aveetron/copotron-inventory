from django.urls import path
from . import views
urlpatterns = [
    path("", views.GrnView.as_view(), name="grn"),
    path("grn-details/", views.GrnDetailView.as_view(), name="grn-details"),
    path("stocks", views.StockView.as_view(), name="stocks"),
    path("stocks/out/", views.StockOutView.as_view(), name="stock-out"),
    path("stocks/out/details/", views.StockDetailsView.as_view(),
         name="stock-details"),
]
