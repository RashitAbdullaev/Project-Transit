from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from .models import Request
from django.views.generic.base import TemplateView
from django.contrib.auth.models import Group,User
from .form import MyCustomUserCreatingForm, RequestForm
from django.contrib.auth.mixins import LoginRequiredMixin


# отображение заявок
class Request_all(TemplateView):
    template_name = 'transit/request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_p'] = Group.objects.get(pk=2)
        context['group_v'] = Group.objects.get(pk=1)
        context['request_all'] = Request.objects.all()
        return context


class CustomSuccessMessageMixin:

    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


# добавление заявок
class Request_create(CustomSuccessMessageMixin, CreateView):
    model = Request
    template_name = 'transit/request_create.html'
    form_class = RequestForm
    success_url = reverse_lazy('request')
    success_msg = 'Заявка создана'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class Request_update(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Request
    template_name = 'transit/request_update.html'
    form_class = RequestForm
    success_url = reverse_lazy('request')
    success_msg = 'Заявка успешно обнавлена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class Request_delete(LoginRequiredMixin, DeleteView, CustomSuccessMessageMixin):
    model = Request
    template_name = 'transit/request_delete.html'
    success_url = reverse_lazy('request')
    success_msg = 'Заявка удалена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_request'] = Request.objects.filter(pk=self.kwargs['pk'])
        for i in context['delete_request']:
            if self.request.user != i.author :
                return self.handle_no_permission()
        context['url'] = self.kwargs['pk']
        return context


# регистрация пользователя
class Create_user(CreateView):
    template_name = 'transit/signup.html'
    form_class = MyCustomUserCreatingForm
    success_url = reverse_lazy('request')

    def post(self, request, *args, **kwargs):
        form = MyCustomUserCreatingForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user.save()
            user_group = Group.objects.get(name=form.cleaned_data['groups'])
            user.groups.add(user_group)
            user = authenticate(username=name,
                                password=password)
            login(request, user)
            return redirect('request')
        else:
            return render(request, self.template_name, {'form': form})

