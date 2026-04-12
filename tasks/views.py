from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from .filters import TaskFilter

from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/show.html"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class TaskDeletePermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks")


class TaskDeleteView(TaskDeletePermissionMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно удалена")
        return super().form_valid(form)
