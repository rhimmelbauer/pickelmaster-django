from django import forms
from match.models import MatchModel, ResultModel
from player.models import PlayerModel


class MatchForm(forms.ModelForm):

    class Meta:
        model = MatchModel
        exclude = ["result", "players"]


class ResultForm(forms.ModelForm):
    winners = forms.ModelMultipleChoiceField(queryset=PlayerModel.objects.all())
    losers = forms.ModelMultipleChoiceField(queryset=PlayerModel.objects.all())

    class Meta:
        model = ResultModel
        fields = "__all__"
