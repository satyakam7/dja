# Generated by Django 2.0.6 on 2018-06-08 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=300)),
                ('link', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True)),
                ('short_des', models.CharField(blank=True, max_length=300)),
                ('logo_link', models.CharField(blank=True, max_length=500)),
                ('image_link', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='LiveMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField(verbose_name='time started')),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('secy', 'Secretary'), ('exe', 'Executive'), ('fac', 'Faculty'), ('cap', 'Captain'), ('vicecap', 'Vice-Captain')], default='secy', max_length=8)),
                ('name', models.CharField(help_text='Full Name', max_length=30)),
                ('entryno', models.CharField(blank=True, help_text='Leave Blank if faculty', max_length=15)),
                ('mobileno', models.CharField(blank=True, help_text='Mobile Number', max_length=15)),
                ('email', models.CharField(help_text='Email ID', max_length=30)),
                ('hostel', models.CharField(blank=True, help_text='Leave Blank if faculty', max_length=15)),
                ('fb', models.CharField(blank=True, help_text='Not required', max_length=200)),
                ('image_link', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='LiveMatch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainSite.LiveMatch'),
        ),
    ]