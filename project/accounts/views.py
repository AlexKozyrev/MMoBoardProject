from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .forms import SignUpForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        common_user_group = Group.objects.get(name='common users')
        user.groups.add(common_user_group)
        return super().form_valid(form)
