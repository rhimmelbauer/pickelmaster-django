# Generated by Django 4.2.6 on 2023-12-01 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionmodel',
            name='awards',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
