# Generated by Django 4.0 on 2021-12-28 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_image_url_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(default='https://st2.depositphotos.com/1561359/12101/v/950/depositphotos_121012076-stock-illustration-blank-photo-icon.jpg', null=True),
        ),
    ]