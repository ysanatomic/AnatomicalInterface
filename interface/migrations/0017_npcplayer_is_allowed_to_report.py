# Generated by Django 3.2.5 on 2021-08-13 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0016_report_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='npcplayer',
            name='is_allowed_to_report',
            field=models.BooleanField(default=True),
        ),
    ]