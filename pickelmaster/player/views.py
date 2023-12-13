from typing import Any

from django.db import models
from player.models import PlayerModel
from django.views.generic import DetailView, TemplateView
from django_tables2.views import SingleTableView
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from player.forms import PlayerForm
from player.tables import PlayerTable, PlayerXWinningCountTable, PartnerLoseOrWinCounterTable


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
        context['table'] = PlayerXWinningCountTable(self.get_table_data(PlayerModel.objects.all()))
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
            } for player in PlayerModel.objects.all()
        ]


class PlayerDetailView(UpdateView):
    template_name = 'player.html'
    form_class = PlayerForm
    model = PlayerModel
    queryset = PlayerModel.objects.all()

    # def process_table_values(self, data):
    #     winner_stats = self.object.get_best_partners()
    #     loser_stats = self.object.get_worst_partners()
    #     table_data = []

    #     players = list(winner_stats.keys() | loser_stats.keys())

    #     for player in players:
    #         table_data.append(
    #             {
    #                 "name": player,
    #                 "win_counter": winner_stats.get(player, 0),
    #                 "lose_counter": loser_stats.get(player, 0)
    #             }
    #         )

    #     return table_data

    def process_table_values(self, data):
        table_data = []

        for key, value in data.items():
            table_data.append(
                {
                    "name": key,
                    "counter": value
                }
            )
            
        return table_data
    
    def get_object(self):
        return PlayerModel.objects.get(username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['partner_win_table'] = PartnerLoseOrWinCounterTable(self.process_table_values(self.object.get_best_partners()))
        context['partner_lose_table'] = PartnerLoseOrWinCounterTable(self.process_table_values(self.object.get_worst_partners()))

        return context

    def post(self, request, **kwargs):
        player_form = PlayerForm(request.POST, request.FILES, instance=self.get_object())

        if player_form.is_valid():
            player_form.save()
            
        return redirect('players')
