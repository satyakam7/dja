# Generated by Django 2.0.6 on 2020-05-29 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0006_juniorexe_pride'),
    ]

    operations = [
        migrations.CreateModel(
            name='swimmingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Full Name', max_length=30)),
                ('entryno', models.CharField(blank=True, max_length=15)),
                ('hostel', models.CharField(blank=True, help_text='Hostel Name', max_length=30)),
                ('mobileno', models.CharField(blank=True, help_text='Mobile Number', max_length=15)),
                ('email', models.CharField(help_text='Email ID', max_length=30)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=15)),
                ('slot', models.CharField(choices=[('slotTTS_67AM', 'slotTTS_67AM'), ('slotTTS_78AM', 'slotTTS_78AM'), ('slotTTS_89AM', 'slotTTS_89AM'), ('slotTTS_56PM', 'slotTTS_56PM'), ('slotTTS_67PM', 'slotTTS_67PM'), ('slotTTS_78PM', 'slotTTS_78PM'), ('slotWFS_67AM', 'slotWFS_67AM'), ('slotWFS_78AM', 'slotWFS_78AM'), ('slotWFS_89AM', 'slotWFS_89AM'), ('slotWFS_56PM', 'slotWFS_56PM'), ('slotWFS_67PM', 'slotWFS_67PM'), ('slotWFS_78PM', 'slotWFS_78PM')], default='slotTTS_67AM', max_length=20)),
                ('image', models.ImageField(blank=True, upload_to='Swimming_forms')),
            ],
        ),
        migrations.AlterField(
            model_name='people',
            name='team',
            field=models.CharField(blank=True, choices=[('', 'None'), ('Athletics (Men)', 'Athletics (Men)'), ('Athletics (Women)', 'Athletics (Women)'), ('Aquatics (Men)', 'Aquatics (Men)'), ('Aquatics (Women)', 'Aquatics (Women)'), ('Badminton (Men)', 'Badminton (Men)'), ('Badminton (Women)', 'Badminton (Women)'), ('Basketball (Men)', 'Basketball (Men)'), ('Basketball (Women)', 'Basketball (Women)'), ('Cricket', 'Cricket'), ('Football', 'Football'), ('Hockey', 'Hockey'), ('Lawn Tennis (Men)', 'Lawn Tennis (Men)'), ('Lawn Tennis (Women)', 'Lawn Tennis (Women)'), ('Squash', 'Squash'), ('Table Tennis (Men)', 'Table Tennis (Men)'), ('Table Tennis (Women)', 'Table Tennis (Women)'), ('Volleyball (Men)', 'Volleyball (Men)'), ('Volleyball (Women)', 'Volleyball (Women)'), ('Weight-lifting', 'Weight-lifting')], default='', help_text='Leave blank if not capn or vice-capn', max_length=20),
        ),
    ]
