from rest_framework import serializers
from apps.task.models import Task


class TaskListTodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"