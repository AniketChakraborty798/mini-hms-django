from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # ROOT REDIRECT
    path('', lambda request: redirect('login')),

    path('', include('users.urls')),
    path('', include('doctors.urls')),
    path('', include('bookings.urls')),
]
