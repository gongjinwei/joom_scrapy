from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from tools.viewsets import CreateOnlyViewSet
from . import serializers,models
from .tasks import add

from celery.result import AsyncResult


class FetchViewSets(ModelViewSet):
    serializer_class = serializers.ItemUrlSerializer
    queryset = models.ItemUrl.objects.all()


class AddView(CreateOnlyViewSet):
    serializer_class = serializers.AddSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = add.apply_async(kwargs={**serializer.validated_data})

        return Response(result.task_id)


class TaskQueryView(CreateOnlyViewSet):
    serializer_class = serializers.TaskQuerySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_id = serializer.validated_data['task_id']
        result=AsyncResult(task_id).get()

        return Response(result)
