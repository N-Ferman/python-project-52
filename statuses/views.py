from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect


from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменен")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Статус успешно удален")
        except ProtectedError:
            messages.error(request, "Невозможно удалить статус")
        return redirect(self.success_url)
