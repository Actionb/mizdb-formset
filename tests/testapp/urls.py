from django.urls import path

from tests.testapp.views import ContactView

urlpatterns = [
    path("edit/<path:pk>", ContactView.as_view(), name="contact"),
]
