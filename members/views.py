from django.shortcuts import render

from .forms import BenefitForm

# Create your views here.
def dashboardView(request):
    context = {
        
        'navbar':True,
    }
    return render(request, 'members/dashboard.html', context)


def benefitView(request):
    context = {
        'form': BenefitForm(),
    }
    if request.method == 'POST':
        pass
    else:
        return render(request, 'members/benefit.html', context)


def benefitListView(request):
    context = {}
    return render(request, 'members/benefitList.html', context)