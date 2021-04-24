from django.urls import path
from .views import FacebookLogin


urlpatterns = [
    path('api/auth/facebook/', FacebookLogin.as_view(), name="fb_login")
]
