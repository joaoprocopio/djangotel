from django.urls import path

from rastro.users.interfaces import views

urlpatterns = [
    path("sign_up", views.sign_up, name="sign_up"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_out", views.sign_out, name="sign_out"),
    path("me", views.current_user, name="current_user"),
    path(
        "password_reset/request",
        views.request_password_reset,
        name="request_password_reset",
    ),
    path("password_reset/confirm", views.reset_password, name="reset_password"),
    path("email_verification/confirm", views.verify_email, name="verify_email"),
]
