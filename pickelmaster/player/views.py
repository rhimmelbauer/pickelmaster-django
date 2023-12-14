from typing import Any

from django.db import models
from player.models import PlayerModel
from django.views.generic import DetailView, TemplateView
from django_tables2.views import SingleTableView
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from player.forms import PlayerForm
from player.tables import PlayerTable, PlayerXWinningCountTable, PartnerWinsAndLostsTable


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
    queryset = PlayerModel.objects.all()

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

        wins_table = PartnerWinsAndLostsTable(self.object.get_partner_ratios())
        # wins_table.columns['counter'].verbose_name = "Wins"

        # lose_table = PartnerWinsAndLostsTable(self.object.get_worst_partners())
        # lose_table.columns['counter'].verbose_name = "Lost"
        
        context['partner_win_table'] = wins_table
        # context['partner_lose_table'] = lose_table

        return context

    def post(self, request, **kwargs):
        player_form = PlayerForm(request.POST, request.FILES, instance=self.get_object())

        if player_form.is_valid():
            player_form.save()
            
        return redirect('players')
