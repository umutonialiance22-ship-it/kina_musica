from django.urls import path
from .views import ArtistStatView, ChannelLinkListCreateView, TrendAlertListView

urlpatterns = [
    path('stats/', ArtistStatView.as_view()),
    path('channels/', ChannelLinkListCreateView.as_view()),
    path('alerts/', TrendAlertListView.as_view()),
]