# Generated by Django 2.0.5 on 2018-06-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='rival_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
