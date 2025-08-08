from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.
def login_view(request):
    context = {
        'navbar':False,
    }
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Change 'home' to your desired redirect
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/loginform.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')  # Change 'login' to your desired redirect


def registerView(request):
    
    context = {
        'form': RegisterForm(),
    }
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            context['form'] = form
            return render(request, 'accounts/register.html', context)
    else:
        return render(request, 'accounts/register.html', context)