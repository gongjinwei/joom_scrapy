# Generated by Django 2.1.2 on 2018-10-23 15:52

from decimal import Decimal
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=1024)),
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
            name='ItemSkuLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_sku', models.CharField(blank=True, max_length=255, null=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('msrp', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('main_image', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.IntegerField(blank=True, null=True)),
                ('variantId', models.CharField(blank=True, max_length=50, null=True)),
                ('inStock', models.BooleanField(blank=True, null=True)),
                ('createdTimeMs', models.BigIntegerField(blank=True, null=True)),
                ('publishedTimeMs', models.BigIntegerField(blank=True, null=True)),
                ('shippingPrice', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('shippingWeight', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
            ],
            options={
                'db_table': 'item_sku_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ItemUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_str', models.TextField(blank=True, null=True)),
                ('source_id', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.IntegerField(blank=True, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('item_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'item_url',
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
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=255)),
                ('platform_id', models.IntegerField(blank=True, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('client_id', models.CharField(blank=True, max_length=255, null=True)),
                ('client_secret', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField()),
                ('access_token', models.TextField(blank=True, null=True)),
                ('refresh_token', models.TextField(blank=True, null=True)),
                ('already', models.IntegerField(blank=True, null=True)),
                ('sync_time', models.IntegerField(blank=True, null=True)),
                ('down_url', models.CharField(blank=True, max_length=255, null=True)),
                ('job_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'shop',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WishShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('createtime', models.IntegerField(blank=True, null=True)),
                ('modifytime', models.IntegerField(blank=True, null=True)),
                ('du_time', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('num', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'wish_shop',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WishVariantItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_sku', models.CharField(blank=True, max_length=255, null=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=1, max_digits=10)),
                ('msrp', models.DecimalField(decimal_places=1, default=Decimal('0'), max_digits=10)),
                ('main_image', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.IntegerField(blank=True, null=True)),
                ('sku', models.CharField(blank=True, max_length=50, null=True)),
                ('variantId', models.CharField(blank=True, max_length=50, null=True)),
                ('shippingPrice', models.DecimalField(decimal_places=1, max_digits=10)),
                ('shipping_time', models.CharField(blank=True, max_length=40, null=True)),
                ('all_images', models.TextField(null=True)),
                ('enabled', models.BooleanField(null=True)),
            ],
            options={
                'db_table': 'wish_shop_item_sku',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='XiciProxy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=16)),
                ('port', models.IntegerField()),
                ('address', models.CharField(max_length=50, null=True)),
                ('protocol', models.CharField(default='http', max_length=5)),
                ('available', models.BooleanField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('check_time', models.DateTimeField(null=True)),
                ('response_time', models.FloatField(null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WishCrawlProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('msrp', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('sale_num', models.IntegerField(blank=True, null=True)),
                ('default_img', models.CharField(blank=True, max_length=255, null=True)),
                ('list_img', models.TextField(blank=True, null=True)),
                ('introduce', models.TextField(blank=True, null=True)),
                ('score1', models.IntegerField(blank=True, null=True)),
                ('score2', models.IntegerField(blank=True, null=True)),
                ('score3', models.IntegerField(blank=True, null=True)),
                ('score4', models.IntegerField(blank=True, null=True)),
                ('score5', models.IntegerField(blank=True, null=True)),
                ('average_score', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('cate', models.CharField(max_length=255)),
                ('parent_sku', models.CharField(max_length=50, null=True)),
                ('url', models.CharField(max_length=255)),
                ('create_time', models.IntegerField()),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('shop_id', models.IntegerField()),
                ('source_id', models.CharField(max_length=255)),
                ('date_uploaded', models.DateField(null=True)),
                ('is_promoted', models.BooleanField(blank=True, null=True)),
                ('tags', jsonfield.fields.JSONField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(null=True)),
                ('number_saves', models.IntegerField(null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('owner_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('review_status', models.CharField(blank=True, max_length=10, null=True)),
                ('py_sku', models.CharField(blank=True, max_length=50, null=True)),
                ('user_ids', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'wish_shop_item',
            },
        ),
    ]
