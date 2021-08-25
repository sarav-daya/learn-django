from django.urls import path
from users import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("register/", views.register_user, name="register"),
    
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.user_profile, name="user-profile"),
    path("account/", views.user_account, name="account"),
]
