# Generated by Django 2.0.6 on 2020-05-30 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0010_swimminguser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swimminguser',
            name='entryno',
            field=models.CharField(blank=True, default='NON-STUDENT', max_length=15),
        ),
        migrations.AlterField(
            model_name='swimminguser',
            name='hostel',
            field=models.CharField(blank=True, default='NON-STUDENT', help_text='Hostel Name', max_length=30),
        ),
    ]
