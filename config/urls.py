from django.urls import path
from django.contrib.auth.views import LogoutView
from home.views import StaffLoginView, index, portal

urlpatterns = [
    path("", index, name="home"),
    path("login/", StaffLoginView.as_view(), name="login"),
    path("portal/", portal, name="portal"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
