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