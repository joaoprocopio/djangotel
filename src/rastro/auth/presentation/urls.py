# urls.py
from django.urls import path

from rastro.auth.presentation import views

urlpatterns = [
    path("me", views.MeView.as_view()),  # type: ignore
    path("signin", views.SignInView.as_view()),  # type: ignore
    path("signup", views.SignUpView.as_view()),  # type: ignore
    path("signout", views.SignOutView.as_view()),  # type: ignore
]
