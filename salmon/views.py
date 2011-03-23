from django.http import HttpResponse
from django.views.decorators.http import require_POST


@require_POST
def endpoint(request):
    return HttpResponse('endpoint')
