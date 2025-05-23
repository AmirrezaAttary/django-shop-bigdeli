# Generated by Django 4.2.20 on 2025-05-06 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('order', '0003_alter_couponmodel_used_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payment.paymentmodel'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='status',
            field=models.IntegerField(choices=[(1, 'در انتظار پرداخت'), (2, 'در حال پردازش'), (3, 'لغو شده')], default=1),
        ),
    ]
