from tests.testapp.views import ContactView
from django.urls import path

urlpatterns = [
    path("edit/<path:pk>", ContactView.as_view(), name="contact"),
]
