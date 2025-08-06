from django.shortcuts import render

# Create your views here.
def dashboardView(request):
    context = {
        'navbar':True,
    }
    return render(request, 'members/dashboard.html', context)