from . import views
from rest_framework import routers

app_name = "api-v1"

router = routers.DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")

urlpatterns = router.urls
