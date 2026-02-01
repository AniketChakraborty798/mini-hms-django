from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from .models import User

GOOGLE_SCOPES = ["https://www.googleapis.com/auth/calendar"]
GOOGLE_REDIRECT_URI = "http://127.0.0.1:8000/google/callback/"


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        if User.objects.filter(username=username).exists():
            return render(request, 'users/signup.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        login(request, user)
        return redirect('redirect-dashboard')

    return render(request, 'users/signup.html')


def user_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('redirect-dashboard')

        return render(request, 'users/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'users/login.html')


@login_required
def google_login(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )

    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes=True,
    )

    request.session["google_state"] = state
    return redirect(auth_url)


@login_required
def google_callback(request):
    state = request.session.get("google_state")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=GOOGLE_SCOPES,
        state=state,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    creds = flow.credentials
    user = request.user

    user.google_access_token = creds.token
    user.google_refresh_token = creds.refresh_token
    user.google_token_expiry = creds.expiry
    user.save()

    return redirect('redirect-dashboard')


@login_required
def redirect_dashboard(request):
    if request.user.role == 'doctor':
        return redirect('doctor-dashboard')
    return redirect('patient-dashboard')


def user_logout(request):
    logout(request)
    return redirect('login')
