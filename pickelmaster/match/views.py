from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import FormMixin
from match.models import SessionModel, MatchModel
from match.forms import MatchForm, ResultForm


class SessionListView(ListView):
    template_name = 'sessions.html'
    model = SessionModel

    def get_queryset(self):
        return SessionModel.objects.all()


class SessionCreateView(CreateView):
    model = SessionModel


class MatchListView(ListView):
    template_name = "matchs.html"
    model = MatchModel


class MatchCreateView(TemplateView):
    template_name = "match_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result_form"] = ResultForm()
        context["match_form"] = MatchForm()
        return context
    
    def post(self, request, *args, **kwargs):
        result_form = ResultForm(request.POST)
        match_form = MatchForm(request.POST)

        if not result_form.is_valid() and not match_form.is_valid():
            context = self.get_context_data(**kwargs)
            context['result_form'] = result_form
            context["match_form"] = match_form

            return render(request, self.template_name, context)
        
        result = result_form.save()
        match = match_form.save(commit=False)

        match.result = result
        match.save()
        match.players.add(*[player for player in result.winners.all()])
        match.players.add(*[player for player in result.losers.all()])

        return redirect(reverse('matches'))
