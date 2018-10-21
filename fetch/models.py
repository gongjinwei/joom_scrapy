from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from jsonfield import JSONField

# Create your models here.


class ItemSkuLog(models.Model):
    source_id = models.CharField(max_length=255, blank=True, null=True)
    sub_sku = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    main_image = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    variantId= models.CharField(max_length=50,blank=True,null=True)
    inStock = models.BooleanField(blank=True,null=True)
    createdTimeMs = models.BigIntegerField(null=True,blank=True)
    publishedTimeMs = models.BigIntegerField(null=True,blank=True)
    shippingPrice = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    shippingWeight=models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))

    class Meta:
        managed = False
        db_table = 'item_sku_log'


class ItemUrl(models.Model):
    url_str = models.TextField(blank=True, null=True)
    source_id = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    item_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_url'


class ItemLog(models.Model):
    goods_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    sale_num = models.IntegerField(default=0)
    default_img = models.CharField(max_length=255, blank=True, null=True)
    list_img = models.TextField(blank=True, null=True)
    introduce = models.TextField(blank=True, null=True)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    score3 = models.IntegerField(default=0)
    score4 = models.IntegerField(default=0)
    score5 = models.IntegerField(default=0)
    average_score = models.DecimalField(max_digits=10, decimal_places=1, default=Decimal(0.0))
    cate = models.CharField(max_length=255)
    source_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    create_time = models.IntegerField()
    date_uploaded = models.IntegerField(blank=True, null=True)
    storeId = models.CharField(max_length=50,blank=True,null=True)
    tags = JSONField(null=True,blank=True)

    class Meta:
        managed = False
        db_table = 'item_log'


# class UserTask(models.Model):
#     user = models.ForeignKey(to=User,on_delete=models.CASCADE)
#     create_time = models.DateTimeField(auto_now_add=True)
#     task_id = models.CharField(max_length=40)

class JoomStore(models.Model):
    storeId = models.CharField(max_length=50,null=True)
    updatedTimeMerchantMs = models.BigIntegerField(null=True)
    enabled=models.BooleanField(null=True)
    enabledByMerchant=models.BooleanField(null=True)
    rating = models.FloatField(null=True)
    name = models.CharField(max_length=255,null=True)
    positiveReviewsCount=models.IntegerField(null=True)
    favoritesCount=models.IntegerField(null=True)
    productsCount=models.IntegerField(null=True)
    reviewsCount = models.IntegerField(null=True)

    class Meta:
        db_table='joom_stroe'


class WishShop(models.Model):
    shop_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    createtime = models.IntegerField(blank=True, null=True)
    modifytime = models.IntegerField(blank=True, null=True)
    du_time = models.CharField(max_length=20, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wish_shop'


class Shop(models.Model):
    shop_name = models.CharField(max_length=255)
    platform_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    already = models.IntegerField(blank=True, null=True)
    sync_time = models.IntegerField(blank=True, null=True)
    down_url = models.CharField(max_length=255, blank=True, null=True)
    job_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop'


class WishCrawlProduct(models.Model):
    goods_name = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal(0.00))
    msrp = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    sale_num = models.IntegerField(default=0)
    default_img = models.CharField(max_length=255, blank=True, null=True)
    list_img = models.TextField(blank=True, null=True)
    introduce = models.TextField(blank=True, null=True)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    score3 = models.IntegerField(default=0)
    score4 = models.IntegerField(default=0)
    score5 = models.IntegerField(default=0)
    average_score = models.DecimalField(max_digits=10, decimal_places=1, default=Decimal(0.0))
    cate = models.CharField(max_length=255,null=True)
    source_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    create_time = models.IntegerField(null=True)
    date_uploaded = models.DateField(null=True)
    tags = JSONField(null=True, blank=True)
    is_promoted = models.BooleanField(null=True,blank=True)
    review_status= models.CharField(max_length=12,null=True,blank=True)
    last_updated = models.DateTimeField(null=True)
    parent_sku = models.CharField(max_length=50,null=True)
    number_saves = models.IntegerField(null=True)
    shop_id = models.IntegerField()

    class Meta:
        db_table = 'wish_crawl_product'


class WishVariantItem(models.Model):
    source_id = models.CharField(max_length=255, blank=True, null=True)
    sub_sku = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    msrp = models.DecimalField(max_digits=10, decimal_places=1, default=Decimal(0.0))
    main_image = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    variantId = models.CharField(max_length=50, blank=True, null=True)
    shippingPrice =models.DecimalField(max_digits=10, decimal_places=1)
    shipping_time = models.CharField(max_length=40,null=True,blank=True)
    all_images = models.TextField(null=True)
    enabled = models.BooleanField(null=True)

    class Meta:
        db_table = 'wish_variant_item'