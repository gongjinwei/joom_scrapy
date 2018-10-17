# -*- coding:UTF-8 -*-

from . import models

from rest_framework import serializers


class ItemUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemUrl
        fields = '__all__'


class StartScrapeSerializer(serializers.Serializer):
    start = serializers.BooleanField()


class AddSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()

class TaskQuerySerializer(serializers.Serializer):
    task_id = serializers.CharField(max_length=40,help_text='任务ID')