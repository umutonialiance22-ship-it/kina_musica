from django.urls import path
from .views import LyricsDetailView

urlpatterns = [
    path('<int:song_id>/', LyricsDetailView.as_view()),
]