# Generated by Django 4.2.20 on 2025-04-04 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimagemodel',
            options={},
        ),
        migrations.AlterModelOptions(
            name='productmodel',
            options={},
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='avg_rate',
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='brief_description',
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='discount_percent',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='WishlistProductModel',
        ),
    ]
