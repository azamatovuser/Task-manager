from rest_framework import generics
from apps.task.models import Task
from apps.task.serializers import TaskListTodaySerializer, TaskSerializer
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView


class TaskAPIListToday(generics.ListAPIView):
    serializer_class = TaskListTodaySerializer

    def get_queryset(self):
        today = now().date()
        return Task.objects.filter(
            account=self.request.user,
            is_done=False,
            created_date__date=today
        )



class TasksDoneTodayCountView(APIView):
    def get(self, request, *args, **kwargs):
        today = now().date()
        count = Task.objects.filter(
            account=request.user,
            is_done=True,
            created_date__date=today
        ).count()
        return Response({"tasks_done_today": count})

class TasksNotStartedTodayCountView(APIView):
    def get(self, request, *args, **kwargs):
        today = now().date()
        count = Task.objects.filter(
            account=request.user,
            is_done=False,
            created_date__date=today
        ).count()
        return Response({"tasks_not_started_today": count})


class TasksInProcessListAPIView(generics.ListAPIView):
    serializer_class = TaskListTodaySerializer

    def get_queryset(self):
        today = now().date()
        return Task.objects.filter(
            account=self.request.user,
            is_done=False,
            created_date__date=today
        )


class TasksDoneListAPIView(generics.ListAPIView):
    serializer_class = TaskListTodaySerializer

    def get_queryset(self):
        today = now().date()
        return Task.objects.filter(
            account=self.request.user,
            is_done=True,
            created_date__date=today
        )


class TaskDeleteAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer