from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from flights_app import views
from flights_app.views import signup, me

router = DefaultRouter()

urlpatterns = [
    path('auth/login', TokenObtainPairView.as_view()),
    path('auth/refresh', TokenRefreshView.as_view()),
    path('auth/signup', signup),
    path('auth/me', me),
    path('auth/users', views.get_users_by_name)
]

urlpatterns.extend(router.urls)
