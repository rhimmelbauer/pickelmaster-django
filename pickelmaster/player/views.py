from typing import Any
from player.models import PlayerModel
from django.views.generic import DetailView, TemplateView
from django_tables2.views import SingleTableView
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from player.forms import PlayerForm
from player.tables import PlayerTable, PlayerXWinningCountTable


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_table_data(self, queryset):
        return [
            {
                'name': player.username,
                'ratio': player.get_last_x_winning_percent(),
            } for player in queryset.all()
        ]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['table'] = PlayerXWinningCountTable(self.get_table_data(PlayerModel.objects.filter(is_active=True)))

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
            } for player in PlayerModel.objects.filter(is_active=True)
        ]


class PlayerDetailView(UpdateView):
    template_name = 'player.html'
    form_class = PlayerForm
    model = PlayerModel

    def post(self, request, **kwargs):
        player_form = PlayerForm(request.POST, request.FILES, instance=self.get_object())

        if player_form.is_valid():
            player_form.save()
            
        return redirect('players')
