from django.urls import path
from . import views
from rest_framework import routers

app_name = "api-v1"

router = routers.DefaultRouter()
router.register('post',views.PostModelViewSet,basename='post')
router.register('category',views.CategoryModelViewSet,basename='category')

urlpatterns = router.urls

# urlpatterns = [
#     path('post/',views.post_list_view,name = "post-list"),
#     path('post/<int:id>/',views.post_detail_view,name = "post-detail"),
#     path('post/<int:pk>/',views.PostSingleApiView.as_view(),name='post-single'),
#     path('post/',views.PostViewSet.as_view({'get':'list'}),name= "post-list"),
#     path('post/<int:pk>/',views.PostViewSet.as_view({'get':'retrieve'}),name= "post-detail"),
# ]