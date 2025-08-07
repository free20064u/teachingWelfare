from django.shortcuts import render

# Create your views here.
def chairDashboardView(request):
    context = {}
    return render(request, 'chair/dashboard.html', context)