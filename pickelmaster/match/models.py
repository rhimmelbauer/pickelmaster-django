from django.db import models
from django.conf import settings
from player.models import PlayerModel


class SessionModel(models.Model):
    date = models.DateField()
    location = models.CharField(verbose_name="Locations", max_length=100)
    awards = models.JSONField()

    def __str__(self):
        return f"pk: {self.pk} - date: {self.date}"
    
    def players(self):
        players = {}
        for match in self.match.all():
            for player in match.players.all():

                players[player.pk] = player

        return players.values()

    def get_total_matches(self):
        return self.match.count()
    
    def get_total_points(self):
        return sum([match.result.winner_score + match.result.losers_score for match in self.match.all()])
    
    def get_ranking(self):
        players = self.players()
        session_ranking = {player.username: {'name': player.username, 'match_count': 0, 'wins': 0, 'lost': 0, 'ratio': '', 'total_points': 0} for player in players}

        for match in self.match.all():
            for player in match.players.all():
                session_ranking[player.username]['match_count'] += 1

                if player in match.result.winners.all():
                    session_ranking[player.username]['wins'] += 1
                    session_ranking[player.username]['total_points'] += match.result.winner_score
                
                if player in match.result.losers.all():
                    session_ranking[player.username]['lost'] += 1
                    session_ranking[player.username]['total_points'] += match.result.losers_score

        for player_ranking in session_ranking.values():
            player_ranking['ratio'] = (player_ranking['wins'] / player_ranking['match_count']) * 100

        return session_ranking


class ResultModel(models.Model):
    winners = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Winners", related_name="winners", blank=True)
    losers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Lossers", related_name="losers", blank=True)
    winner_score = models.IntegerField()
    losers_score = models.IntegerField()

    def __str__(self) -> str:
        winners = [player.username for player in self.winners.all()]
        losers = [player.username for player in self.losers.all()]
        return f"pk: {self.pk} - Winners: {winners} - Losers: {losers}"


class MatchModel(models.Model):
    result = models.ForeignKey(ResultModel, related_name="result", verbose_name="Result", blank=True, null=True, on_delete=models.CASCADE)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='players', verbose_name="Match Players", blank=True)
    session = models.ForeignKey(SessionModel, related_name="match", verbose_name="Session", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        players = [player.username for player in self.players.all()]
        return f"pk: {self.pk} - session: {self.session} - players: {players}" if self.session else self.pk
