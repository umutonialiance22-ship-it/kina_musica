from django.urls import path
from .views import SongListView, TrendingSongsView, LiveSongsView, SongUploadView

urlpatterns = [
    path('', SongListView.as_view()),
    path('trending/', TrendingSongsView.as_view()),
    path('live/', LiveSongsView.as_view()),
    path('upload/', SongUploadView.as_view()),
]
