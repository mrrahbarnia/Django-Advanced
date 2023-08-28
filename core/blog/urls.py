from django.urls import path,include
from blog import views

app_name = "blog"

urlpatterns = [
    # path('cbv-index/',views.IndexView.as_view(),name = "cbv-index"),
    # path('go-to-index/',views.RedirectView.as_view(),name='go-to-index'),
    path('posts/',views.PostListView.as_view(),name="posts"),
    path('posts/<int:pk>',views.DetalViewPost.as_view(),name='detail-post'),
    path('posts/createpost/',views.CreatePostView.as_view(),name='create-post'),
    path('posts/<int:pk>/edit',views.UpdatePostView.as_view(),name='edit-post'),
    path('posts/<int:pk>/delete/',views.DeletePostView.as_view(),name="delete-post"),
    path('api/v1/',include("blog.api.v1.urls")),
]