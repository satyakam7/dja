# Generated by Django 2.0.6 on 2020-10-05 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0019_auto_20200808_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='type',
            field=models.CharField(choices=[('Secretary', 'Secretary'), ('Executive', 'Executive'), ('Junior Executive', 'Junior Executive'), ('Faculty', 'Faculty'), ('Captain', 'Captain'), ('Vice-Captain', 'Vice-Captain'), ('General Secretary', 'General Secretary'), ('Deputy General Secretary', 'Deputy General Secretary')], default='Secretary', max_length=40),
        ),
    ]
