
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


def user_profile_image_path(instance, filename):
    return f"profile/{filename}"


class PlayerModel(AbstractUser):
    aka = models.CharField(verbose_name="AKA", max_length=80, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_profile_image_path, blank=True)

    objects = UserManager()

    class Meta:
        ordering = ["username"]

    def get_matches_count(self):
        return self.players.count()
    
    def get_wins_count(self):
        return self.winners.count()

    def get_lose_count(self):
        return self.losers.count()
    
    def get_winning_percent(self):
        if self.players.count():
            return (self.winners.count() / self.players.count()) * 100

    def get_last_x_winning_percent(self, x=13):
        matches = self.players.all().order_by('-session__date')[:x]
        wins = sum([1 for match in matches if self in match.result.winners.all()])

        return (wins / x) * 100
    
    def get_best_partners(self):
        winners = []
        winner_counter = []

        for match in self.players.all():
            for winner in match.result.winners.all():
                if winner != self and winner.username:
                    winners.append(winner.username)
        
        for winner in set(winners):
            wins = winners.count(winner)
            matchs = len([match for match in self.players.all() for player in match.players.all() if player.username == winner])
            winner_counter.append(
                {
                    'name': winner,
                    'count': wins,
                    'matches': matchs,
                    'ratio': (wins / matchs) * 100
                }
            )
                
        return winner_counter

    def get_worst_partners(self):
        losing_players = []
        lose_counter = []

        for match in self.players.all():
            for loser in match.result.losers.all():
                if loser != self and loser.username:
                    losing_players.append(loser.username)
        
        for loser in set(losing_players):
            lost_count = losing_players.count(loser)
            matchs = len([match for match in self.players.all() for player in match.players.all() if player.username == loser])
            lose_counter.append(
                {
                    'name': loser,
                    'count': lost_count,
                    'matches': matchs,
                    'ratio': (lost_count / matchs) * 100
                }
            )
                
        return lose_counter

    def get_nemesis(self):
        ...

