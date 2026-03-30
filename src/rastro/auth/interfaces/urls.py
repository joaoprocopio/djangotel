from django.urls import path

from rastro.auth.interfaces import views

urlpatterns = [
    path("me", views.me, name="me"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("sign_out", views.sign_out, name="sign_out"),
]
