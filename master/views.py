from django.shortcuts import render

# Create your views here.
def masterDashboardView(request):
    context = {}
    return render(request, 'master/dashboard.html', context)