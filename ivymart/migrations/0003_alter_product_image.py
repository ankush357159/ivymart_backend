# Generated by Django 4.0.1 on 2022-02-02 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivymart', '0002_order_shippingaddress_review_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='myimages'),
        ),
    ]
