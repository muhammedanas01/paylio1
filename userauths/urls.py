from django.urls import path 
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("signup/", views.registerview, name="sign-up"),
    path("login/", views.loginview, name="login"),
    path("sign-out/", views.logoutview, name="sign-out")
]