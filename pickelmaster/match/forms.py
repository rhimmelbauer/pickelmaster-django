from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from match.models import MatchModel, ResultModel, SessionModel
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


class SessionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"class": "datepicker"}))

    class Meta:
        model = SessionModel
        fields = "__all__"
