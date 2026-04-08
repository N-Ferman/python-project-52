from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from .forms import UserRegisterForm, UserUpdateForm
# Create your views here.

class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)
    
class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения')
        return redirect('users')
    
class UserUpdateView(UserPermissionMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)
    
class UserDeleteView(UserPermissionMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно удален')
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)