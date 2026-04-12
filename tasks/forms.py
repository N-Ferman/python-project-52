from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['executor'].label_from_instance = (
        lambda user: user.get_full_name() or user.username
    )
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }