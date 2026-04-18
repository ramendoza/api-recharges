"""
URL configuration for recharges project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path

from .views import (
    LoginView,
    ProfileView,
    RechargePricesListView,
    RefreshTokenView,
    SendRechargeView,
    SendRechargesListView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('api/recharges/send/', SendRechargesListView.as_view(), name='send_recharges_list'),
    path('api/recharges/prices/', RechargePricesListView.as_view(), name='recharge_prices_list'),
    path('api/recharges/', SendRechargeView.as_view(), name='send_recharge'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
]
