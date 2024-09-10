from django.urls import path
from apps.task.views import (TaskAPIListToday,
                             TasksDoneTodayCountView,
                             TasksNotStartedTodayCountView,
                             TasksInProcessListAPIView,
                             TasksDoneListAPIView,
                             TaskDeleteAPIView,
                             TaskCreateAPIView,
                             TaskUpdateAPIView)


urlpatterns = [
    path("tasks_for_today/", TaskAPIListToday.as_view()),
    path('done_today_count/', TasksDoneTodayCountView.as_view()),
    path('not_started_today_count/', TasksNotStartedTodayCountView.as_view()),
    path('in_process/', TasksInProcessListAPIView.as_view()),
    path('done/', TasksDoneListAPIView.as_view()),
    path("delete/<int:pk>/", TaskDeleteAPIView.as_view()),
    path("create/", TaskCreateAPIView.as_view()),
    path("update/<int:pk>/", TaskUpdateAPIView.as_view()),
]