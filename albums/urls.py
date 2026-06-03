from django.urls import path
from .views import AlbumListCreateView, AlbumDetailView

urlpatterns = [
    path('', AlbumListCreateView.as_view()),
    path('<int:pk>/', AlbumDetailView.as_view()),
]