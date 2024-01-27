import random

from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import CreateView
from .forms import SignUpForm, VerifyForm
from .models import Code


class SignUp(CreateView): # регистрация
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        common_user_group = Group.objects.get(name='common users')
        user.groups.add(common_user_group)
        code = generate_confirmation_code()
        new_code = Code(user=user, code=code)
        new_code.save()
        send_confirmation_email(user.email, code)
        return super().form_valid(form)


def Verify(request): # верификация
    form = VerifyForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data['code']
        user = request.user
        print(user)
        code_check = Code.objects.filter(user=user).first().code
        print(code_check)
        if code_check == code:
            user.last_name = 'confirmed'
            user.save()
            return redirect('home')
        else:
            # user.is_active = False
            error = 'Код подтверждения почты введен неверно'
            return render(request, 'verify.html', {'error': error, 'form': form})

    return render(request, 'verify.html', {'form': form})


def generate_confirmation_code():
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def send_confirmation_email(email, code):
    from django.core.mail import EmailMessage
    subject = "Подтверждение регистрации"
    message = ("Здравствуйте! Чтобы завершить регистрацию на нашем сайте, пожалуйста, введите код подтверждения: "
               "`{}`").format(
        code)
    from_email = "noreply@example.com"
    to_email = email
    message = EmailMessage(subject, message, from_email, [to_email])
    message.content_subtype = "html"
    message.send()
