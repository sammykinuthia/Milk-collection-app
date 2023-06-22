from django.urls import path, include
from .views import index, get_customers, get_customer, logout_user, pay, daraja
from . import views
urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customers', get_customers),
    path('logout', logout_user),
    path('customers/<str:username>', get_customer),
    path('pay', pay),
    path('daraja', daraja),

    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    # register, confirmation, validation and callback urls
    path('c2b/register', views.register_urls,
         name="register_mpesa_validation"),
    path('c2b/confirmation', views.confirmation, name="confirmation"),
    path('c2b/validation', views.validation, name="validation"),
    path('c2b/callback', views.call_back, name="call_back"),
]
