from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import PostCreateView, ApiView, PostUpdateView, TestView
from .views import PostDeleteView



urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    # path('post/api/', ApiView.as_view(), name='api'),
    path('post/api/<int:cursus_id>/', ApiView.as_view(), name='api'),
    path('post/test/', TestView.as_view(), name='test'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    # path("password_reset", views.password_reset_request, name="password_reset")

]
