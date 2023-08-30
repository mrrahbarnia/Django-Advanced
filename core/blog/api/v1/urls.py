from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    # path('post/',views.post_list_view,name = "post-list"),
    # path('post/<int:id>/',views.post_detail_view,name = "post-detail"),
    path('post/',views.PostListApiView.as_view(),name= "post-list"),
    path('post/<int:id>',views.PostSingleApiView.as_view(),name='post-single'),
    
]