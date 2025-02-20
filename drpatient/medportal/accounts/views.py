# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserProfileForm
from .models import UserProfile


def signup(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to the role-based dashboard
    else:
        form = UserProfileForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print("user :", user)
        if user is not None:
            login(request, user)
            # Redirect based on user role
            try:
                user_profile = UserProfile.objects.get(user=user)
                next_url = request.GET.get('next')
                if next_url:
                    if user_profile.user_type == 'doctor':
                        return redirect('doctor_dashboard')
                    elif user_profile.user_type == 'patient':
                        return redirect('patient_dashboard')
                    else:
                        return redirect(next_url)
                else:
                    return redirect('doctor_dashboard')

            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

@login_required
def dashboard(request):
    """Redirect users to their respective dashboards"""
    if request.user.user_type == "doctor":
        return redirect('doctor_dashboard')
    elif request.user.user_type == "patient":
        return redirect('patient_dashboard')
    return redirect('login')

@login_required
def doctor_dashboard(request):
    return render(request, 'accounts/doctor_dashboard.html', {'user': request.user})

@login_required
def patient_dashboard(request):
    return render(request, 'accounts/patient_dashboard.html', {'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('login')

