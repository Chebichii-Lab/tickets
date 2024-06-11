# Ticketer/persons/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, TopUpForm
from .models import Person
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from events.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    users = User.objects.all()
    events = Event.objects.all()
    return render(request, 'persons/index.html', {'users': users, 'events': events})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sign up successful. Please log in.')
            return redirect('log_in')
    else:
        form = SignUpForm()
    return render(request, 'persons/sign_up.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the index page upon successful login
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'persons/log_in.html')

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required
def top_up_wallet(request):
    user = request.user
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user.wallet_balance += amount
            user.save()
            messages.success(request, f'Wallet topped up by {amount}.')
            # return redirect('event_list')  # Redirect to the event list after top up
            
            # Redirect back to the purchase ticket page if coming from there
            next_url = request.GET.get('next', 'wallet_balance')
            return redirect(next_url)

    else:
        form = TopUpForm()

    return render(request, 'persons/top_up_wallet.html', {'form': form})

@login_required
def wallet_balance(request):
    user = request.user
    return render(request, 'persons/wallet_balance.html', {'wallet_balance': user.wallet_balance})

