from django.urls import path
from .views import SignUp, Verify

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('verify/', Verify, name='verify'),
]