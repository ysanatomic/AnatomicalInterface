# Generated by Django 3.2.5 on 2021-08-07 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0010_npcplayer_was_last_in'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=20)),
                ('message', models.TextField(max_length=300)),
                ('sent_on', models.DateTimeField()),
            ],
        ),
    ]