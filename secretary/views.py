from django.shortcuts import render

# Create your views here.
def secretaryDashboardView(request):
    context = {}
    return render(request, 'secretary/dashboard.html', context)