from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.feed_view, name='feed'),
    path('<int:pk>/like/', views.PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('<int:pk>/unlike/', views.PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]
