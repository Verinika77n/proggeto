from django.urls import path, include

from .views import blog, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, post_modal_data, modal_like, modal_comment

from profiles.views import signup


urlpatterns = [
    path('', blog.as_view(), name='blog'),
    path('profiles/', include('profiles.urls')),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blog-edit'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    path('<int:pk>/modal/', post_modal_data, name='post-modal-data'),
    path('<int:pk>/modal/like/', modal_like, name='modal-like'),      
    path('<int:pk>/modal/comment/', modal_comment, name='modal-comment'), 
]
