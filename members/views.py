from django.shortcuts import redirect, render

from .forms import BenefitForm, ChildrenForm, EditProfileForm, SpouseForm
from .models import Children, NextOfKin, Parent, Spouse


# Create your views here.
def dashboardView(request):
    member = request.user
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


def profileView(request):
    context = {
        'spouse':Spouse.objects.get(member=request.user),
        'children':Children.objects.filter(member=request.user),
        'parent':Parent.objects.filter(member=request.user),
        'next_of_kin':NextOfKin.objects.filter(member=request.user),
    }
    
    return render(request, 'members/profile.html', context)

def editProfileView(request):
    context = {
        'form': EditProfileForm(instance=request.user),
    }
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print('er')
            print(form.errors)
            return render(request, 'members/editProfile.html', context)    
    else:
        return render(request, 'members/editProfile.html', context)

    
def spouseView(request):
    context = {
        'form': SpouseForm(initial={'member':request.user })
    }
    if request.method == 'POST':
        form = SpouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'members/spouse.html', context)  
    else:
        return render(request, 'members/spouse.html', context)


def childrenView(request):
    context = {
        'form': ChildrenForm(initial={'member': request.user}),
    }
    if request.method == 'POST':
        form = ChildrenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        return render(request, 'members/children.html', context)