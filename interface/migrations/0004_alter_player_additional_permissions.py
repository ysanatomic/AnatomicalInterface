# Generated by Django 3.2.5 on 2021-07-31 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0003_alter_player_additional_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='additional_permissions',
            field=models.ManyToManyField(blank=True, to='interface.Permissions'),
        ),
    ]