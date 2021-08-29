from django.urls import path
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", views.getRoutes),
    path("projects/", views.get_projects),
    path("projects/<str:pk>/", views.get_project),
    path("projects/<str:pk>/vote/", views.vote_project),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
