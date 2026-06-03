from django.urls import path
from .views import (FavoriteListCreateView, HistoryListView, RecordingListCreateView,
    FollowerListCreateView, CommentListCreateView, ReviewListCreateView)

urlpatterns = [
    path('favorites/', FavoriteListCreateView.as_view()),
    path('history/', HistoryListView.as_view()),
    path('recordings/', RecordingListCreateView.as_view()),
    path('follow/', FollowerListCreateView.as_view()),
    path('comments/', CommentListCreateView.as_view()),
    path('reviews/', ReviewListCreateView.as_view()),
]