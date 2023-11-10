from typing import Any
from player.models import PlayerModel
from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from player.forms import PlayerForm
 
class HomeView(TemplateView):
    template_name = 'home.html'


class PlayerListView(ListView):
    template_name = 'players.html'
    model = PlayerModel

    def get_queryset(self):
        return PlayerModel.objects.all()


class PlayerDetailView(UpdateView):
    template_name = 'player.html'
    form_class = PlayerForm
    model = PlayerModel


    def post(self, request, **kwargs):
        player_form = PlayerForm(request.POST, request.FILES, instance=self.get_object())

        if player_form.is_valid():
            player_form.save()
            
        return redirect('players')

