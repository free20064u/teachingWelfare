from django.shortcuts import redirect, render

from .forms import BenefitForm, ChildrenForm, EditProfileForm, NextOfKinForm, ParentForm, SpouseForm
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
        'form': BenefitForm(initial={'member':request.user}),
    }
    if request.method == 'POST':
        form = BenefitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, 'members/benefit.html', context)
    else:
        return render(request, 'members/benefit.html', context)


def benefitListView(request):
    context = {}
    return render(request, 'members/benefitList.html', context)


def profileView(request):
    try:
        spouse = Spouse.objects.get(member=request.user)
    except:
        spouse = None
    
    try:
        parent = Parent.objects.get(member=request.user)
    except:
        parent = None

    try:
        next_of_kin = NextOfKin.objects.get(member=request.user)
    except:
        next_of_kin = None

    context = {
        'spouse': spouse,
        'children':Children.objects.filter(member=request.user),
        'parent':parent,
        'next_of_kin':next_of_kin,
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
    

def parentView(request):
    context = {
        'form': ParentForm(initial={'member': request.user}),
    }
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        return render(request, 'members/children.html', context)


def nextOfKinView(request):
    context = {
        'form': NextOfKinForm(initial={'member': request.user}),
    }
    if request.method == 'POST':
        form = NextOfKinForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        return render(request, 'members/nextOfKin.html', context)