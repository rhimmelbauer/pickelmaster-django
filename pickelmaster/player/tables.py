import django_tables2 as tables

from player.models import PlayerModel


class PlayerTable(tables.Table):
    name = tables.Column(verbose_name="Name")
    match_count = tables.Column()
    wins = tables.Column()
    lost = tables.Column()
    ratio = tables.Column(verbose_name="Win Percent")

    class Meta:
        template_name = "includes/custom_dt2_bootstrap4.html"
        fields = ("name", "match_count", "wins", "lost", "ratio")
        order_by = ['-ratio']

    def render_ratio(self, value):
        return "{:0.2f}%".format(value)