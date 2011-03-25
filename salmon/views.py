from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def endpoint(request):
    print 'slapped: %s' % (request.raw_post_data,)
    return HttpResponse('slapped: %s' % (request.raw_post_data,))
