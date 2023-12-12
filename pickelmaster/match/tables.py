import django_tables2 as tables

from match.models import MatchModel


class MatchTable(tables.Table):
    class Meta:
        model = MatchModel
        template_name = "includes/custom_dt2_bootstrap4.html"
        fields = ("pk", "session", "players", "result__winners", "result__losers")


class SessionSummeryTable(tables.Table):
    name = tables.Column(verbose_name="Name")
    match_count = tables.Column()
    wins = tables.Column()
    lost = tables.Column()
    ratio = tables.Column(verbose_name="Win Percent")
    total_points = tables.Column(verbose_name="Points Scored")

    class Meta:
        order_by = ['-ratio', '-total_points']
        template_name = "includes/custom_dt2_bootstrap4.html"

    def render_ratio(self, value):
        return "{:0.2f}%".format(value)
