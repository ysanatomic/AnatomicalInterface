# Generated by Django 3.2.5 on 2021-08-12 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0012_chatmessage_sent_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='npcplayer',
            name='uuid',
            field=models.UUIDField(default=None, null=True, unique=True),
        ),
    ]
