from django.urls import path
from .views import (
    signup,
    user_login,
    user_logout,
    redirect_dashboard,
    google_login,
    google_callback,
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', redirect_dashboard, name='redirect-dashboard'),

    # Google Calendar OAuth
    path('google/login/', google_login, name='google-login'),
    path('google/callback/', google_callback, name='google-callback'),
]
