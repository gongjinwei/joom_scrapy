# Generated by Django 2.1.2 on 2018-10-16 14:18

from decimal import Decimal
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fetch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('msrp', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('sale_num', models.IntegerField(default=0)),
                ('default_img', models.CharField(blank=True, max_length=255, null=True)),
                ('list_img', models.TextField(blank=True, null=True)),
                ('introduce', models.TextField(blank=True, null=True)),
                ('score1', models.IntegerField(default=0)),
                ('score2', models.IntegerField(default=0)),
                ('score3', models.IntegerField(default=0)),
                ('score4', models.IntegerField(default=0)),
                ('score5', models.IntegerField(default=0)),
                ('average_score', models.DecimalField(decimal_places=1, default=Decimal('0'), max_digits=10)),
                ('cate', models.CharField(max_length=255)),
                ('source_id', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('create_time', models.IntegerField()),
                ('date_uploaded', models.IntegerField(blank=True, null=True)),
                ('storeId', models.CharField(blank=True, max_length=50, null=True)),
                ('tags', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'item_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JoomStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeId', models.CharField(max_length=50, null=True)),
                ('updatedTimeMerchantMs', models.BigIntegerField(null=True)),
                ('enabled', models.BooleanField(null=True)),
                ('enabledByMerchant', models.BooleanField(null=True)),
                ('rating', models.FloatField(null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('positiveReviewsCount', models.IntegerField(null=True)),
                ('favoritesCount', models.IntegerField(null=True)),
                ('productsCount', models.IntegerField(null=True)),
                ('reviewsCount', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'joom_stroe',
            },
        ),
    ]
