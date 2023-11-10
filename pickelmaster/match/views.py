from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from match.models import SessionModel, MatchModel
from match.forms import MatchForm, ResultForm, SessionForm


class SessionListView(ListView):
    template_name = 'sessions.html'
    model = SessionModel

    def get_queryset(self):
        return SessionModel.objects.all()


class SessionCreateView(FormView):
    template_name = 'session.html'
    model = SessionModel
    form_class = SessionForm
    success_url = reverse_lazy("sessions")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SessionDetailView(DetailView):
    template_name = 'session.html'
    model = SessionModel


class SessionFormView(SingleObjectMixin, FormView):
    template_name = 'session.html'
    form_class = SessionForm
    model = SessionModel


class SessionView(View):

    def get(self, request, *args, **kwargs):
        view = SessionDetailView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, **kwargs):
        view = SessionFormView.as_view()
        return view(request, **kwargs)


class SessionSummaryView(DetailView):
    template_name = 'session_summary.html'
    model = SessionModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




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
