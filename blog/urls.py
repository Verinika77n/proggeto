from django.urls import path, include

from .views import blog, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('', blog.as_view(), name='blog'),
    path('profiles/', include('profiles.urls')),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blog-edit'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),

]
