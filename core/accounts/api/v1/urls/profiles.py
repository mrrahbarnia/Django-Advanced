from django.urls import path

from .. import views


urlpatterns = [
    # Get user profiles
    path("", views.ProfileAPIView.as_view(), name="profile"),
]
