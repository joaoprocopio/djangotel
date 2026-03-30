# type: ignore
from django.middleware.csrf import CsrfViewMiddleware, get_token


class EnsureCsrfCookie(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        retval = super().process_view(request, callback, callback_args, callback_kwargs)
        get_token(request)
        return retval
