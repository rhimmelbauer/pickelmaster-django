from django.contrib import admin

from match.models import SessionModel, MatchModel, ResultModel


class SessionModelAdmin(admin.ModelAdmin):
    ...


class MatchModelAdmin(admin.ModelAdmin):
    ...


class ResultModelAdmin(admin.ModelAdmin):
    ...


admin.site.register(SessionModel, SessionModelAdmin)
admin.site.register(MatchModel, MatchModelAdmin)
admin.site.register(ResultModel, ResultModelAdmin)
