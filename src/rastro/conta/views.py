from django.http import JsonResponse


def conta(request):
    return JsonResponse(data={"my": 123})
