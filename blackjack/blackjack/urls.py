"""blackjack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tables import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
	path('', views.HomeView.as_view(), name='homepage'),
    path('accounts/register/', views.RegisterView.as_view(), name="register"),
	path('accounts/login/', views.LoginView.as_view(), name="login"),
	path('accounts/logout/', login_required(views.LogoutView.as_view()), name='logout'),
    path('deposit/', login_required(views.DepositView.as_view()), name='deposit'),
	path('deposit/checkout/?amount=<amount>/?currency=<currency>', login_required(views.PayPalCheckOutView.as_view()), name='deposit_checkout'),
    path('withdraw/',login_required(views.WithdrawView.as_view()), name='withdraw'),
	path('withdraw/checkout', views.PayPalCheckOutView.as_view(), name='withdraw_checkout'),
	path('tables/balance/', login_required(views.GetUserBalance.as_view()), name = 'get_low_balance'),
	path('tables/game_balance/', login_required(views.GetGameBalance.as_view()), name = 'get_game_balance'),
	path('tables/leave/', login_required(views.LeaveTableView.as_view()), name = 'leave_table'),
 	path('tables/table_sit/', login_required(views.SitView.as_view()), name = 'table_sit'),
	path('tables/low/', login_required(views.LowTableView.as_view()), name="low"),
	path('tables/medium/', login_required(views.MediumTable.as_view()), name="medium"),
	path('tables/high/', login_required(views.HighTable.as_view()), name="high"),
	path('tables/vip/', login_required(views.VipTable.as_view()), name="vip"),
]
