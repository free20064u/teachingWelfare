from django.shortcuts import render

# Create your views here.
def financeDashboardView(request):
    context = {}
    return render(request, 'finance/dashboard.html', context)