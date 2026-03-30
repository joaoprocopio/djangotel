import random

from django.views import View


class TaskListView(View):
    def get(self, request):
        # TODO: list current user assigned tasks
        pass

    def post(self, request):
        # TODO: create task
        pass


class TaskDetailView(View):
    def get(self, request, task_id):
        # TODO: get a task for a task id, user must be owner
        pass

    def put(self, request, task_id):
        # TODO: update a task, if the user is a owner
        pass

    def delete(self, request, task_id):
        # TODO: delete a task, if the user is a owner
        pass


class AlwaysBreakView(View):
    def get(self, request):
        # TODO: extract a domain error
        raise Exception("This always breaks")


class Break50PercentView(View):
    def get(self, request):
        # TODO: extract a domain error
        if random.random() < 0.5:
            raise Exception("50% break")


class BreakRandomlyView(View):
    def get(self, request):
        # TODO: extract a domain error
        if random.random() < random.random():
            raise Exception("Random break")
