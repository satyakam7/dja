# Generated by Django 2.0.6 on 2021-03-13 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0026_coachfeedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReimbursementForms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Full Name', max_length=30)),
                ('image', models.ImageField(blank=True, upload_to='ReimbursementForms')),
                ('email', models.CharField(help_text='Email', max_length=30)),
                ('uid', models.CharField(help_text='UID', max_length=30)),
                ('status', models.CharField(default=1, help_text='UID', max_length=30)),
            ],
        ),
    ]
