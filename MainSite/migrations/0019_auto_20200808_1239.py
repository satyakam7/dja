# Generated by Django 2.0.6 on 2020-08-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0018_auto_20200629_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juniorexe',
            name='team',
            field=models.CharField(blank=True, choices=[('', 'None'), ('Athletics (Men)', 'Athletics (Men)'), ('Athletics (Women)', 'Athletics (Women)'), ('Aquatics (Men)', 'Aquatics (Men)'), ('Aquatics (Women)', 'Aquatics (Women)'), ('Badminton (Men)', 'Badminton (Men)'), ('Badminton (Women)', 'Badminton (Women)'), ('Basketball (Men)', 'Basketball (Men)'), ('Basketball (Women)', 'Basketball (Women)'), ('Cricket', 'Cricket'), ('Football', 'Football'), ('Hockey', 'Hockey'), ('ISC', 'ISC'), ('Lawn Tennis (Men)', 'Lawn Tennis (Men)'), ('Lawn Tennis (Women)', 'Lawn Tennis (Women)'), ('Squash (Men)', 'Squash (Men)'), ('Squash (Women)', 'Squash (Women)'), ('Table Tennis (Men)', 'Table Tennis (Men)'), ('Table Tennis (Women)', 'Table Tennis (Women)'), ('Volleyball (Men)', 'Volleyball (Men)'), ('Volleyball (Women)', 'Volleyball (Women)'), ('Weight-lifting', 'Weight-lifting')], default='', help_text='Leave blank if not capn or vice-capn', max_length=20),
        ),
        migrations.AlterField(
            model_name='people',
            name='team',
            field=models.CharField(blank=True, choices=[('', 'None'), ('Athletics (Men)', 'Athletics (Men)'), ('Athletics (Women)', 'Athletics (Women)'), ('Aquatics (Men)', 'Aquatics (Men)'), ('Aquatics (Women)', 'Aquatics (Women)'), ('Badminton (Men)', 'Badminton (Men)'), ('Badminton (Women)', 'Badminton (Women)'), ('Basketball (Men)', 'Basketball (Men)'), ('Basketball (Women)', 'Basketball (Women)'), ('Cricket', 'Cricket'), ('Football', 'Football'), ('Hockey', 'Hockey'), ('ISC', 'ISC'), ('Lawn Tennis (Men)', 'Lawn Tennis (Men)'), ('Lawn Tennis (Women)', 'Lawn Tennis (Women)'), ('Squash (Men)', 'Squash (Men)'), ('Squash (Women)', 'Squash (Women)'), ('Table Tennis (Men)', 'Table Tennis (Men)'), ('Table Tennis (Women)', 'Table Tennis (Women)'), ('Volleyball (Men)', 'Volleyball (Men)'), ('Volleyball (Women)', 'Volleyball (Women)'), ('Weight-lifting', 'Weight-lifting')], default='', help_text='Leave blank if not capn or vice-capn', max_length=20),
        ),
    ]