# Generated by Django 3.1.1 on 2021-10-24 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affordances', '0002_auto_20211022_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='item_type',
            field=models.CharField(default='critical', max_length=80),
            preserve_default=False,
        ),
    ]
