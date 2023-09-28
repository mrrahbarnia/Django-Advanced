from django.urls import path, include
from .views import email, caching

app_name = "accounts"

urlpatterns = [
    path("send-email/", email, name="send-email"),
    path('caching/', caching, name="caching"),
    path("", include("django.contrib.auth.urls")),
    path("api/v1/", include("accounts.api.v1.urls")),
    # path('api/v2/', include('djoser.urls')),
    # path('api/v2/', include('djoser.urls.jwt')),
]
