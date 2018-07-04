# Generated by Django 2.0.6 on 2018-07-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0010_auto_20180619_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='rival',
            name='team_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]