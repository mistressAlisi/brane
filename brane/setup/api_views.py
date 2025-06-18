from django.http import JsonResponse


def install_exec_handle(request):
    return JsonResponse({"res":"ok"},safe=False)