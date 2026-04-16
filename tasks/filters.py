import django_filters
from django import forms

from statuses.models import Status
from labels.models import Label
from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус",
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field("executor").remote_field.model.objects.all(),
        label="Исполнитель",
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label="Метка",
        widget=forms.SelectMultiple(),
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        label="Только свои задачи",
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
