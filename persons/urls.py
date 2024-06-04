# TicketPlatform/Persons/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import top_up_wallet, wallet_balance, index, sign_up, log_in, log_out

urlpatterns = [
    path('', index, name='index'),
    path('sign-up/', sign_up, name='sign_up'),
    path('log-in/', log_in, name='log_in'),
    path('logout/', log_out, name='logout'),
    path('top-up/', top_up_wallet, name='top_up_wallet'),
    path('balance/', wallet_balance, name='wallet_balance'),
]
