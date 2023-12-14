
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

        for match in self.players.filter(result__winners__in=[self]):
            if self in match.result.winners.all():
                for winner in match.result.winners.all():
                    if winner != self:
                        winners.append(winner)
        
        for winner in set(winners):
            wins = winners.count(winner)
            matches = [m for m in self.players.all() if winner in m.result.winners.all()]
            
            winner_counter.append(
                {
                    'name': winner,
                    'count': wins,
                    'matches': len(matches),
                    'ratio': (wins / len(matches)) * 100
                }
            )
                
        return winner_counter

    def get_worst_partners(self):
        losing_players = []
        lose_counter = []

        for match in self.players.filter(result__losers__in=[self]):
            if self in match.result.losers.all():
                for loser in match.result.losers.all():
                    if loser != self:
                        losing_players.append(loser)
        
        for loser in set(losing_players):
            lost_count = losing_players.count(loser)
            matches = [m for m in self.players.all() if loser in m.result.losers.all() and self in m.result.losers.all()]
            
            lose_counter.append(
                {
                    'name': loser.username,
                    'count': lost_count,
                    'matches': len(matches),
                    'ratio': (lost_count / len(matches)) * 100
                }
            )

        return lose_counter
    
    def get_partner_ratios(self):
        wining_partners = []
        losing_partners = []
        partners_result = []

        for match in self.players.all():
            match_winners = match.result.winners.all()
            match_losers = match.result.losers.all()
            
            wining_partners.extend([player for player in match_winners if player != self and self in match_winners])
            losing_partners.extend([player for player in match_losers if player != self and self in match_losers])

        for player in set(wining_partners + losing_partners):
            wins = wining_partners.count(player)
            losts = losing_partners.count(player)
            matches = wins + losts

            partners_result.append({
                "name": player.username,
                "wins": wins,
                "losts": losts,
                "matches": matches,
                "ratio": (wins / matches) * 100
            })
        
        return partners_result

    def get_nemesis(self):
        ...

