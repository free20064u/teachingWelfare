from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def login_view(request):
    context = {
        'navbar':False,
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change 'home' to your desired redirect
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/loginform.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')  # Change 'login' to your desired redirect