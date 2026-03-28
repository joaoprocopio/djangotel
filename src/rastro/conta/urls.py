from django.urls import path

from rastro.conta import views

urlpatterns = [
    path("", views.conta),
]
