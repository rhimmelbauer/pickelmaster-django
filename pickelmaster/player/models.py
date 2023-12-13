
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

        for match in self.players.all():
            for winner in match.result.winners.all():
                if winner != self:
                    winners.append(winner.username)
        
        winner_counter = {}
        for winner in winners:
            if winner not in winner_counter:
                winner_counter[winner] = winners.count(winner)
                
        return winner_counter

    def get_worst_partners(self):
        lose = []

        for match in self.players.all():
            for lost in match.result.losers.all():
                if lost != self:
                    lose.append(lost.username)
        
        lose_counter = {}
        for lost in lose:
            if lost not in lose_counter:
                lose_counter[lost] = lose.count(lost)
                
        return lose_counter

    def get_nemesis(self):
        ...

