# Generated by Django 3.1.1 on 2021-10-24 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affordances', '0005_auto_20211024_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='binarychoice',
            name='item',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
