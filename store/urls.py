from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", login_required(views.StoreView.as_view()), name="store"),
    path(
        "details",
        login_required(views.StoreDetailsView.as_view()),
        name="store-details",
    ),
]
