from django.urls import path, include

from .views import blog, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, mark_notifications_as_read
from profiles.views import signup


urlpatterns = [
    path('', blog.as_view(), name='blog'),
    path('profiles/', include('profiles.urls')),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blog-edit'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
   path('mark-notifications-read/', mark_notifications_as_read, name='mark_notifications_read'),
]
