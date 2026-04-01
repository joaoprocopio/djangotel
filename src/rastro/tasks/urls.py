from django.urls import path

from rastro.tasks import views

urlpatterns = [
    path("", views.TaskListView.as_view()),  # type: ignore
    path("<int:task_id>", views.TaskDetailView.as_view()),  # type: ignore
    path("always-break", views.AlwaysBreakView.as_view()),  # type: ignore
    path("break-50-percent", views.Break50PercentView.as_view()),  # type: ignore
    path("break-randomly", views.BreakRandomlyView.as_view()),  # type: ignore
]
