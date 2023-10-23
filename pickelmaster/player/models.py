
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class PlayerModel(AbstractUser):
    aka = models.CharField(verbose_name="AKA", max_length=80)
    # avatar = models.ImageField(upload_to=user_profile_avatar_path, blank=True) 

    objects = UserManager()

    def get_matches_count(self):
        return self.players.count()
    
    def get_wins_count(self):
        return self.winners.count()

    def get_lose_count(self):
        return self.losers.count()
    
    def get_winning_percent(self):
        return (self.winners.count() / self.players.count()) * 100
