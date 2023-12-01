
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


def user_profile_image_path(instance, filename):
    return f"profile/{filename}"


class PlayerModel(AbstractUser):
    aka = models.CharField(verbose_name="AKA", max_length=80, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_profile_image_path, blank=True)
    active = models.BooleanField(default=True)

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
