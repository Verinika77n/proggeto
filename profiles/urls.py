from django.urls import path

from .views import EntryListView, EntryDetailView, EntryCreateView, EntryUpdateView, EntryDeleteView

from .views import signup

urlpatterns = [
    path('', EntryListView.as_view(), name='profiles'),
    path('<int:pk>/', EntryDetailView.as_view(), name='profiles-detail'),
    path('create/', EntryCreateView.as_view(), name='profiles-create'),
    path('<int:pk>/edit/', EntryUpdateView.as_view(), name='profiles-edit'),
    path('<int:pk>/delete/', EntryDeleteView.as_view(), name='profiles-delete'),
    path('signup/', signup, name='signup'),
]
