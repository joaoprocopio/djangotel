from django.urls import path

from rastro.auth.presentation import views

urlpatterns = [
    path("csrftoken", views.CsrfTokenView.as_view()),
    path("me", views.MeView.as_view()),
    path("signin", views.SignInView.as_view()),
    path("signup", views.SignUpView.as_view()),
    path("signout", views.SignOutView.as_view()),
]
