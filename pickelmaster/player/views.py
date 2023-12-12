from typing import Any
from player.models import PlayerModel
from django.views.generic import DetailView, TemplateView
from django_tables2.views import SingleTableView
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from player.forms import PlayerForm
from player.tables import PlayerTable
 
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['players'] = PlayerModel.objects.all()
        return context

class PlayerListView(SingleTableView):
    template_name = 'players.html'
    model = PlayerModel
    table_class = PlayerTable

    def get_queryset(self):
        return [
            {
                'name': player.username,
                'match_count': player.get_matches_count(),
                'wins': player.get_wins_count(),
                'lost': player.get_lose_count(),
                'ratio': player.get_winning_percent(),
            } for player in PlayerModel.objects.all()]

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['session_table'] = SessionSummeryTable(self.object.get_ranking())
    #     context['matches_table'] = MatchTable(self.object.match.all())
    #     return context
    


class PlayerDetailView(UpdateView):
    template_name = 'player.html'
    form_class = PlayerForm
    model = PlayerModel


    def post(self, request, **kwargs):
        player_form = PlayerForm(request.POST, request.FILES, instance=self.get_object())

        if player_form.is_valid():
            player_form.save()
            
        return redirect('players')

