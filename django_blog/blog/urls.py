from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('posts/', views.PostListView.as_view(), name='post-list-posts'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add-comment'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='update-comment'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete-comment'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts-by-tag'),
    path('search/', views.SearchListView.as_view(), name='search-posts'),
    path('register/', views.register, name='register'),


    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]
