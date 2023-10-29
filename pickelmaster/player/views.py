from player.models import PlayerModel
from django.views.generic import DetailView, ListView
 

class PlayerListView(ListView):
    template_name = 'players.html'
    model = PlayerModel

    def get_queryset(self):
        return PlayerModel.objects.all()

class PlayerModelDetailView(DetailView):
    model = PlayerModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['']
        return context