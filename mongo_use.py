# -*- coding:UTF-8 -*-
import MySQLdb

dbparams = dict(
    host='122.226.65.250',
    db='cjdn_newyiliao',
    user='cjdn_newyiliao',
    passwd='GPnGmibX6QGGzbDA',
    port=39306,
    charset='utf8mb4',
    use_unicode=True)
connect = MySQLdb.connect(**dbparams)
cursor = connect.cursor()
sql = """
                INSERT INTO wish_shop_item_s1(goods_name,sale_num,default_img,list_img,introduce,source_id,url,date_uploaded,last_updated,tags,parent_sku,is_promoted,review_status,number_saves,shop_id,create_time,enabled,price,msrp)\n                VALUES (\'Health &amp; Beauty Home Use Massage Care Oval Egg Shape Pedicure Foot File Ped Egg Callus Cuticle Remover Foot Care 119XP002757\',0,\'https://contestimg.wish.com/api/webimage/5927f1359b141d6873b77d14-original.jpg?cache_buster=0ddf306b8c9baff54229540d332c8633\',\'https://contestimg.wish.com/api/webimage/5927f1359b141d6873b77d14-1-original.jpg|https://contestimg.wish.com/api/webimage/5927f1359b141d6873b77d14-2-original.jpg|https://contestimg.wish.com/api/webimage/5927f1359b141d6873b77d14-3-original.jpg|https://contestimg.wish.com/api/webimage/5927f1359b141d6873b77d14-4-original.jpg|https://contestimg.wish.com/api/webimage/5927f1359b141d6873b77d14-5-original.jpg|https://contestimg.wish.com/api/webimage/5927f1359b141d6873b77d14-6-original.jpg\',\'1. Over 135 Precision Micro Files\\n2. Safe to Touch\\n3. Ergonomic Design\\n4. Cuticle Saving part makes no mess\\n\\nMaterial: ABS\\nShape: Oval\\nSize: 5.3*6*10cm\\n\\nPackage Included:\\n1 * Ped Egg\\n1 * Grinding Film\',\'5927f1359b141d6873b77d14\',\'https://www.wish.com/product/5927f1359b141d6873b77d14\',\'2017-05-26 00:00:00\',\'2018-09-14 17:39:50\',\'[{\\"Tag\\": {\\"id\\": \\"beauty\\", \\"name\\": \\"Beauty\\"}}, {\\"Tag\\": {\\"id\\": \\"homeliving\\", \\"name\\": \\"Home &amp; Living\\"}}, {\\"Tag\\": {\\"id\\": \\"pedicurefootspa\\", \\"name\\": \\"Pedicure &amp; Foot Spas\\"}}, {\\"Tag\\": {\\"id\\": \\"healthbeauty\\", \\"name\\": \\"Health &amp; Beauty\\"}}, {\\"Tag\\": {\\"id\\": \\"cuticleremover\\", \\"name\\": \\"Cuticle Removers\\"}}, {\\"Tag\\": {\\"id\\": \\"massagetool\\", \\"name\\": \\"Massage Tools\\"}}, {\\"Tag\\": {\\"id\\": \\"precision\\", \\"name\\": \\"Precision\\"}}, {\\"Tag\\": {\\"id\\": \\"homekitchen\\", \\"name\\": \\"Home &amp; Kitchen\\"}}, {\\"Tag\\": {\\"id\\": \\"eggshaped\\", \\"name\\": \\"egg shaped\\"}}, {\\"Tag\\": {\\"id\\": \\"massage\\", \\"name\\": \\"Massage\\"}}]\',\'119XP002757\',0,\'approved\',\'0\',512,1540917756,0,\'3.00\',\'30.0\')"""
cursor.execute(sql)
connect.commit()

connect.close()
