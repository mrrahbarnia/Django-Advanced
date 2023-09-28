from django.http import (
    HttpResponse, JsonResponse
)
from django.views.decorators.cache import cache_page

import requests

from .tasks import send_email

def email(request):
    send_email.delay()
    return HttpResponse("<h1>Done</h1>")

@cache_page(60)
def caching(request):
    r = requests.get("https://30ad6a60-9542-46ac-a2c0-1005df1c504a.mock.pstmn.io/test/5")
    return JsonResponse(r.json())