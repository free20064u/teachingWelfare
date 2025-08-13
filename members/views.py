from django.shortcuts import redirect, render
from django.db.models import Sum
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import BenefitForm, ChildrenForm, EditProfileForm, NextOfKinForm, ParentForm, SpouseForm
from .models import Children, NextOfKin, Parent, Spouse
from finance.models import Dues
from secretary.models import Announcement


# Create your views here.
@login_required
def dashboardView(request):
    member = request.user

    # Calculate the member's total contribution from all their dues payments.
    total_contribution = Dues.objects.filter(member=member).aggregate(total=Sum('amount'))['total'] or 0.00

    # Determine the member's payment status for the current month.
    today = timezone.now().date()
    has_paid_this_month = Dues.objects.filter(
        member=member,
        payment_date__year=today.year,
        payment_date__month=today.month
    ).exists()

    if has_paid_this_month:
        payment_status = "Up to Date"
        payment_status_class = "text-success"
    else:
        payment_status = "Outstanding"
        payment_status_class = "text-warning"

    # Get the 5 most recent payments for the activity feed.
    recent_payments = Dues.objects.filter(member=member).order_by('-payment_date')[:5]

    # Get announcements that the logged-in member has not yet dismissed.
    unread_announcements = Announcement.objects.exclude(read_by=member)

    context = {
        'navbar':True,
        'total_contribution': total_contribution,
        'payment_status': payment_status,
        'payment_status_class': payment_status_class,
        'recent_payments': recent_payments,
        'unread_announcements': unread_announcements,
    }
    return render(request, 'members/dashboard.html', context)

@login_required
def fundDetailsView(request):
    """
    Displays a paginated and filterable statement of the logged-in
    member's contribution history.
    """
    member = request.user
    
    # Base queryset for all dues related to the member
    all_dues_history = Dues.objects.filter(member=member).order_by('-payment_date')

    # Get unique years for which payments exist, for the filter dropdown
    payment_dates = all_dues_history.dates('payment_date', 'year', order='DESC')
    available_years = [date.year for date in payment_dates]

    # Get the selected year from the URL query parameter for filtering
    selected_year_str = request.GET.get('year')
    dues_for_display = all_dues_history
    selected_year = None

    if selected_year_str and selected_year_str.isdigit():
        selected_year = int(selected_year_str)
        dues_for_display = all_dues_history.filter(payment_date__year=selected_year)

    # Calculate the total for the displayed period and the grand total
    total_dues_period = dues_for_display.aggregate(total=Sum('amount'))['total'] or 0.00
    grand_total_dues = all_dues_history.aggregate(total=Sum('amount'))['total'] or 0.00

    # Add pagination to the dues history
    paginator = Paginator(dues_for_display, 12)  # Show 12 payments per page
    page_number = request.GET.get('page')
    dues_page_obj = paginator.get_page(page_number)

    context = {
        'navbar': True,
        'dues_history': dues_page_obj,
        'total_dues_period': total_dues_period,
        'grand_total_dues': grand_total_dues,
        'available_years': available_years,
        'selected_year': selected_year,
    }
    return render(request, 'members/fund_details.html', context)


@login_required
def benefitView(request):
    if request.method == 'POST':
        form = BenefitForm(request.POST, request.FILES)
        if form.is_valid():
            benefit = form.save(commit=False)
            benefit.member = request.user  # Securely assign the logged-in member
            benefit.save()
            messages.success(request, "Your benefit request has been submitted successfully and is now pending review.")
            return redirect('benefit_list')
    else:
        # For a GET request, create a new, empty form.
        # The member is assigned in the POST logic, not through the form.
        form = BenefitForm()

    context = {
        'form': form,
        'navbar': True,
    }
    return render(request, 'members/benefit.html', context)


@login_required
def benefitListView(request):
    context = {}
    return render(request, 'members/benefitList.html', context)


@login_required
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

@login_required
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

    
@login_required
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


@login_required
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
    

@login_required
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


@login_required
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