from django.urls import path

from rastro.conta.presentation import views

urlpatterns = [
    path("", views.ContaView.as_view()),
    path("csrftoken", views.CsrfTokenView.as_view()),
    path("signin", views.SignInView.as_view()),
    path("signup", views.SignUpView.as_view()),
    path("signout", views.SignOutView.as_view()),
]
