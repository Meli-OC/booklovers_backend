from django.contrib import admin
from django.urls import path, include
# from allauth.socialaccount.providers.google import views as google_views
from authentication.views import GoogleLogin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login')
    # path('auth/', include('authentication.urls'))

]
