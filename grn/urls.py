from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(views.GrnView.as_view()), name="grn"),
    path("grn-details/", login_required(views.GrnDetailView.as_view()), name="grn-details"),
    path("stocks", login_required(views.StockView.as_view()), name="stocks"),
    path("stocks/out/", login_required(views.StockOutView.as_view()), name="stock-out"),
    path("stocks/out/details/", login_required(views.StockDetailsView.as_view()),
         name="stock-details"),
    path("stock/return/<int:stock_out_id>/", login_required(views.StockReturnView.as_view()),
         name="stock-return"),
]
