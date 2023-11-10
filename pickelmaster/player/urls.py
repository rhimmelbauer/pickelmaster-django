from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from player import views
# from catalog import views as catalog_views

urlpatterns = [
    path('players/', views.PlayerListView.as_view(), name='players'),
    path('player/<int:pk>', views.PlayerDetailView.as_view(), name='player')
]