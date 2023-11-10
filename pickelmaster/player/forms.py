from django import forms
from player.models import PlayerModel


class PlayerForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = PlayerModel
        fields = ['aka', 'avatar']
