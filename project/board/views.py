from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

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


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'


class ResponseCreateView(LoginRequiredMixin, CreateView):
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


class AdUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.update_ad',)
    form_class = AdForm
    raise_exception = True
    model = Ad
    template_name = 'ad_edit.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        return super().dispatch(request, *args, **kwargs)


class AdDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_ad',)
    raise_exception = True
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('home')


@login_required
def private_cabinet(request):
    user = request.user
    ads = Ad.objects.filter(user=user)
    responses = Response.objects.filter(ad__in=ads)

    if request.method == "GET":
        action = request.GET.get("action")
        sort_by = request.GET.get("sort_by", "-dateCreation")

        if action == "filter":
            if sort_by == "content":
                responses = responses.order_by("-dateCreation")
            else:
                responses = responses.order_by("-ad__dateCreation")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            response_id = request.POST.get("response_id")
            response = Response.objects.get(id=response_id)
            if response.ad.user == user:
                response.delete()
                return redirect("private_cabinet")

        if action == "accept":
            response_id = request.POST.get("response_id")
            response = Response.objects.get(id=response_id)
            if response.ad.user == user:
                response.accepted = True
                response.save()
                return redirect("private_cabinet")

    return render(
        request,
        "private_cabinet.html",
        {"responses": responses, "sort_by": sort_by},
    )