from django.urls import path
from .views import HomePageView, AdCreate, ResponseCreateView, AdDetailView, private_cabinet, AdUpdate, AdDelete, \
   subscriptions

urlpatterns = [
   path('', HomePageView.as_view(), name='home'),
   path('ad/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
   path('response/<int:pk>/', ResponseCreateView.as_view(), name='response_create'),
   path('pc/', private_cabinet, name='private_cabinet'), # личный кабинет
   path('create/', AdCreate.as_view(), name='ad_create'),
   path('<int:pk>/update/', AdUpdate.as_view(), name='ad_update'),
   path('<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]