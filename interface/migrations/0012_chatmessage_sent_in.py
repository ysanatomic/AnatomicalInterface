# Generated by Django 3.2.5 on 2021-08-07 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0011_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='sent_in',
            field=models.CharField(default='Unknown', max_length=20),
        ),
    ]
