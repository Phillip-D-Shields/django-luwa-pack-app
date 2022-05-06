from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from .models import PackType


class PackListView(LoginRequiredMixin, ListView):
    template_name = 'luwa/pack_list.html'
    model = PackType
    context_object_name = 'user_pack_types'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = PackType.objects.filter(user=self.request.user)
        # TODO add pack type summary
        # TODO add pack query
        return context


class CustomLoginView(LoginView):
    template_name = 'luwa/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('pack_list')


class RegisterView(FormView):
    template_name = 'luwa/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pack_list')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    # prevent authenticated users from accessing registerview
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('pack_list')
        return super(RegisterView, self).get(*args, **kwargs)


class CreatePackTypeView(LoginRequiredMixin, CreateView):
    template_name = 'luwa/pack_type_form.html'
    model = PackType
    fields = ['name', 'description']
    success_url = reverse_lazy('pack_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePackTypeView, self).form_valid(form)
