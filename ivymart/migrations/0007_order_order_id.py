# Generated by Django 4.0.1 on 2022-02-14 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivymart', '0006_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
