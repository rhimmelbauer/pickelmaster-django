from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from player.models import PlayerModel
from match.models import SessionModel
from django.views.generic import DetailView, ListView
 

class PlayerListView(ListView):
    template_name = 'players.html'
    model = PlayerModel

    def get_queryset(self):
        return PlayerModel.objects.all()
    

class SessionListView(ListView):
    template_name = 'sessions.html'
    model = SessionModel

    def get_queryset(self):
        return SessionModel.objects.all()


class PlayerModelDetailView(DetailView):
    model = PlayerModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['']
        return context