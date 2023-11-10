from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from match import views
# from catalog import views as catalog_views

urlpatterns = [
    path('sessions/', views.SessionListView.as_view(), name='sessions'),
    path('session-summary/<int:pk>/', views.SessionSummaryView.as_view(), name='session-summary'),
    path('matchs/', views.MatchListView.as_view(), name="matches"),
    path('match/create/', views.MatchCreateView.as_view(), name='match-create')
]