# Generated by Django 2.0.6 on 2020-10-08 04:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0020_auto_20201005_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='FantasyLeagueMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchCode', models.IntegerField(default=0, help_text='Unique Match Code')),
                ('team1', models.CharField(help_text='Team 1', max_length=30)),
                ('team2', models.CharField(help_text='Team 2', max_length=30)),
                ('startTime', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('activationTime', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('deactivationTime', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='FantasyLeaguePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchCode', models.IntegerField(default=0, help_text='Unique Match Code')),
                ('name', models.CharField(help_text='Player Name', max_length=30)),
                ('team', models.CharField(help_text='Team', max_length=30)),
                ('playerType', models.CharField(choices=[('Batsman', 'Batsman'), ('Bowler', 'Bowler'), ('AllRounder', 'AllRounder')], default='Batsman', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='FantasyLeagueSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchCode', models.IntegerField(default=0, help_text='Unique Match Code')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('entryno', models.CharField(blank=True, max_length=15)),
                ('email', models.CharField(help_text='Email ID', max_length=30)),
                ('submittedString', models.CharField(max_length=1000)),
            ],
        ),
    ]
