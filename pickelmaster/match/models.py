from django.db import models
from django.conf import settings


class SessionModel(models.Model):
    date = models.DateField()
    location = models.CharField(verbose_name="Locations", max_length=100)
    awards = models.JSONField()

    def get_total_matches(self):
        return self.match.count()
    
    def get_total_points(self):
        return sum([match.result.winner_score + match.result.losers_score for match in self.match.all()])
    
    def get_ranking(self):
        sessin_ranking = {}
        for match in self.match.all():
            for winner in match.winners.all():
                if winner not in sessin_ranking:
                    sessin_ranking[winner.usrename] = 0
                sessin_ranking[winner.username] += 1

        return sessin_ranking


class ResultModel(models.Model):
    winners = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Winners", related_name="winners", blank=True)
    losers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Lossers", related_name="losers", blank=True)
    winner_score = models.IntegerField()
    losers_score = models.IntegerField()


class MatchModel(models.Model):
    result = models.ForeignKey(ResultModel, related_name="result", verbose_name="Result", blank=True, null=True, on_delete=models.CASCADE)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='players', verbose_name="Match Players", blank=True)
    session = models.ForeignKey(SessionModel, related_name="match", verbose_name="Session", blank=True, null=True, on_delete=models.CASCADE)
