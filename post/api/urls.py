
from django.urls import path,include
from .views import CommentViewSet, LikeViewSet, LikedApiView, PostComments, PostDetailAV, PostLikes, PostListAV
from rest_framework.routers import DefaultRouter

ROUTER = DefaultRouter()
ROUTER.register("comments", CommentViewSet)
ROUTER.register("likes", LikeViewSet)

urlpatterns = [
    path('posts/', PostListAV.as_view()),
    path('<int:pk>/',PostDetailAV.as_view(),name='post-detail'),  
    path("liked/", LikedApiView.as_view()),
    path("posts/<post_id>/likes", PostLikes.as_view()),
    path("posts/<post_id>/comments", PostComments.as_view()),
    path("", include(ROUTER.urls)), 
]