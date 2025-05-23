# Generated by Django 4.2.20 on 2025-05-04 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_productmodel_discount_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategorymodel',
            name='slug',
            field=models.SlugField(allow_unicode=True),
        ),
        migrations.AlterField(
            model_name='productimagemodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productmodel'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='slug',
            field=models.SlugField(allow_unicode=True),
        ),
    ]
