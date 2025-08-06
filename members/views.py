from django.shortcuts import render

# Create your views here.
def dashboardView(request):
    context = {
        'navbar':True,
    }
    return render(request, 'members/dashboard.html', context)


def benefitView(request):
    context = {}
    if request.method == 'POST':
        pass
    else:
        return render(request, 'members/benefit.html', context)
