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
    sale_num = models.IntegerField(default=0,null=True)
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
    storeId = models.CharField(max_length=50,unique=True)
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
        managed = False
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
    sale_num = models.IntegerField(blank=True, null=True)
    default_img = models.CharField(max_length=255, blank=True, null=True)
    list_img = models.TextField(blank=True, null=True)
    introduce = models.TextField(blank=True, null=True)
    score1 = models.IntegerField(blank=True, null=True,default=0)
    score2 = models.IntegerField(blank=True, null=True,default=0)
    score3 = models.IntegerField(blank=True, null=True,default=0)
    score4 = models.IntegerField(blank=True, null=True,default=0)
    score5 = models.IntegerField(blank=True, null=True,default=0)
    average_score = models.DecimalField(max_digits=10, decimal_places=1,default=Decimal(5.0))
    cate = models.CharField(max_length=255)
    parent_sku = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)
    create_time = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shop_id = models.IntegerField()
    source_id = models.CharField(max_length=255)
    date_uploaded = models.DateField(null=True)
    is_promoted = models.BooleanField(null=True, blank=True)
    tags = JSONField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True)
    number_saves = models.IntegerField(null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    owner_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    review_status = models.CharField(max_length=10, blank=True, null=True)
    py_sku = models.CharField(max_length=50, blank=True, null=True)
    user_ids = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wish_shop_item'


class WishVariantItem(models.Model):
    source_id = models.CharField(max_length=255, blank=True, null=True)
    sub_sku = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.0))
    main_image = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    variantId = models.CharField(max_length=50, blank=True, null=True)
    shippingPrice =models.DecimalField(max_digits=10, decimal_places=2)
    shipping_time = models.CharField(max_length=40,null=True,blank=True)
    all_images = models.TextField(null=True)
    enabled = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'wish_shop_item_sku'


class XiciProxy(models.Model):
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    address = models.CharField(max_length=50,null=True)
    protocol = models.CharField(max_length=5,default='http')
    available = models.BooleanField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    check_time = models.DateTimeField(null=True)
    wish_response_time = models.FloatField(null=True)
    joom_response_time = models.FloatField(null=True)
    joom_access_token = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = 'fetch_xiciproxy'


class WishNewItem(models.Model):
    goods_name = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    msrp = models.DecimalField(max_digits=10, decimal_places=2)
    sale_num = models.IntegerField(blank=True, null=True)
    default_img = models.CharField(max_length=255, blank=True, null=True)
    list_img = models.TextField(blank=True, null=True)
    introduce = models.TextField(blank=True, null=True)
    score1 = models.IntegerField(blank=True, null=True)
    score2 = models.IntegerField(blank=True, null=True)
    score3 = models.IntegerField(blank=True, null=True)
    score4 = models.IntegerField(blank=True, null=True)
    score5 = models.IntegerField(blank=True, null=True)
    average_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cate = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255)
    create_time = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shop_id = models.IntegerField(blank=True, null=True)
    source_id = models.CharField(max_length=255, blank=True, null=True)
    date_uploaded = models.DateField(blank=True, null=True)
    is_promoted = models.IntegerField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    upc = models.CharField(max_length=255, blank=True, null=True)
    landing_page_url = models.CharField(max_length=255, blank=True, null=True)
    owner_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    enabled = models.IntegerField(blank=True, null=True)
    py_sku = models.CharField(max_length=50, blank=True, null=True)
    user_ids = models.CharField(max_length=255, blank=True, null=True)
    variation_id = models.CharField(max_length=50, blank=True, null=True)
    merchant_id = models.CharField(max_length=50, blank=True, null=True)
    merchant_name = models.CharField(max_length=255, blank=True, null=True)
    size_id = models.CharField(max_length=50, blank=True, null=True)
    color_id = models.CharField(max_length=50, blank=True, null=True)
    extra_photo_sequence_id = models.IntegerField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    num_wishes = models.IntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    currently_viewing_nums = models.IntegerField(blank=True, null=True)
    rating_size_summary = models.TextField(blank=True, null=True)
    rating_size_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wish_new_item'


class WishNewItemSku(models.Model):
    source_id = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    main_image = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    variantid = models.CharField(db_column='variantId', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    inventory = models.IntegerField(blank=True, null=True)
    shippingprice = models.DecimalField(db_column='shippingPrice', max_digits=10, decimal_places=2, blank=True,
                                        null=True)  # Field name made lowercase.
    enabled = models.IntegerField(blank=True, null=True)
    extra_photo_sequence_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wish_new_item_sku'


class WishNewProduct(models.Model):
    is_new = models.IntegerField(blank=True, null=True)
    num_bought = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(unique=True, max_length=50)
    true_tag_ids = models.TextField(blank=True, null=True)
    variation_id = models.CharField(max_length=50, blank=True, null=True)
    merchant_id = models.CharField(max_length=50, blank=True, null=True)
    contest_page_picture = models.TextField(blank=True, null=True)
    merchant_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    generation_time = models.BigIntegerField(blank=True, null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sequence_id = models.IntegerField(blank=True, null=True)
    color_id = models.CharField(max_length=30, blank=True, null=True)
    size_id = models.CharField(max_length=30, blank=True, null=True)
    cache_buster = models.CharField(max_length=50, blank=True, null=True)
    total_inventory = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wish_new_product'


class WishShopItemUrl(models.Model):
    url_str = models.TextField(blank=True, null=True)
    source_id = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    item_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wish_shop_item_url'


class JoomCateInfo(models.Model):
    cate_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'joom_cate_info'


class JoomCateProduct(models.Model):
    goods_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_num = models.IntegerField(blank=True, null=True)
    default_img = models.CharField(max_length=255, blank=True, null=True)
    list_img = models.TextField(blank=True, null=True)
    introduce = models.TextField(blank=True, null=True)
    score1 = models.IntegerField(blank=True, null=True)
    score2 = models.IntegerField(blank=True, null=True)
    score3 = models.IntegerField(blank=True, null=True)
    score4 = models.IntegerField(blank=True, null=True)
    score5 = models.IntegerField(blank=True, null=True)
    average_score = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    cate = models.CharField(max_length=255)
    source_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    create_time = models.IntegerField()
    date_uploaded = models.IntegerField(blank=True, null=True)
    storeid = models.CharField(db_column='storeId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tags = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    categoryid = models.CharField(db_column='categoryId', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'joom_cate_product'