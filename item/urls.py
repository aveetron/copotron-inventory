from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("item-type", login_required(views.ItemTypeView.as_view()), name="item-type"),
    path("item-type-detail", login_required(views.ItemTypeDetailsView.as_view()),
         name="item-type-detail"),
    path("", login_required(views.ItemView.as_view()), name="item"),
    path("item-detail", login_required(views.ItemDetailView.as_view()), name="item-detail"),
    path("uom", login_required(views.UomView.as_view()), name="uom"),
    path("uom-detail", login_required(views.UomDetailsView.as_view()), name="uom-detail"),
]
