from django.urls import path
from post.views import index, NewPost, PostDetails, tags, like, favorite

urlpatterns = [
    path('', index, name='index'),
    path('new_post/', NewPost, name = 'newPost'),
    path('<uuid:post_id>/', PostDetails, name='postdetails'),
    path('tag/<slug:tag_slug>', tags, name='tags'),
    path('<uuid:post_id>/like', like, name = 'postlike'),
    path('<uuid:post_id>/favorite', favorite, name = 'postfavorite')
]