# Generated by Django 4.0 on 2021-12-28 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='img',
        ),
        migrations.AddField(
            model_name='listing',
            name='image_URL',
            field=models.URLField(null=True),
        ),
    ]
