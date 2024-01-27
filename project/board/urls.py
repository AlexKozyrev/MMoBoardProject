from django.urls import path
# Импортируем созданное нами представление
from .views import HomePageView, AdCreate, ResponseCreateView

urlpatterns = [
   path('', HomePageView.as_view()),
   path('response/<int:pk>/', ResponseCreateView.as_view(), name='response_create'),
   path('create/', AdCreate.as_view(), name='ad_create'),
]