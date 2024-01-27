from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView

from .forms import AdForm
from .models import Ad, Response


class HomePageView(ListView):
    model = Ad
    template_name = 'home.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')


class ResponseCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_responce',)
    raise_exception = True
    model = Response
    template_name = 'response_create.html'
    fields = ['content']

    def form_valid(self, form):
        form.instance.ad_id = self.kwargs['pk']
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


# Create your views here.

class AdCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_ad',)
    form_class = AdForm
    raise_exception = True
    model = Ad
    # и новый шаблон, в котором используется форма.
    template_name = 'ad_edit.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
