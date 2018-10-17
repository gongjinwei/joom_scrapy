# -*- coding:UTF-8 -*-
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

app_name = 'fetch'
router.register('itemUrl',views.FetchViewSets)
router.register('add',views.AddView,base_name='add')
router.register('taskView',views.TaskQueryView,base_name='taskView')
# router.register('scrape',views.StartScrapeView,base_name='scrape')

urlpatterns = router.urls