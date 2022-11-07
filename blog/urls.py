from django.urls import path
from . import views
from .views import PostCreateView, ApiView, PostUpdateView
from .views import PostDeleteView


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/api/', ApiView.as_view(), name='api'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
]
