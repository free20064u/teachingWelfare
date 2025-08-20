import datetime
import calendar
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator 
from django.db.models import Q, Value, Sum, Max
from django.db.models.functions import Concat, TruncMonth
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounts.models import CustomUser
from members.models import Benefit
from secretary.models import Announcement
from .models import Dues
from .forms import DuesPaymentForm, HonourBenefitForm
from utils.messaging import send_sms

# Create your views here.
@login_required
def financeDashboardView(request):
    # Aggregate total fund balance from all dues payments
    total_fund_balance = Dues.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Count the total number of non-superuser members
    total_members = CustomUser.objects.filter(is_superuser=False, is_active=True).count()

    # Get the 5 most recent dues payments as recent activities
    recent_activities = Dues.objects.select_related('member').order_by('-payment_date')[:5]

    # --- Logic for outstanding members ---
    today = timezone.now().date()
    current_month_year = today.strftime('%B %Y')

    # Calculate total contributions for the current year
    yearly_total_contributions = Dues.objects.filter(
        payment_date__year=today.year
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Calculate total contributions for the current month
    monthly_total_contributions = Dues.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Get IDs of members who have paid in the current month
    paid_this_month_ids = Dues.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).values_list('member_id', flat=True).distinct()

    # Get members who have NOT paid this month, and annotate with their last payment date.
    # The related name from CustomUser to Dues is 'dues' (from member.dues.all()).
    outstanding_members = CustomUser.objects.filter(
        is_superuser=False, is_active=True
    ).exclude(
        pk__in=paid_this_month_ids
    ).annotate(
        last_payment_date=Max('dues__payment_date')
    ).order_by('last_name', 'first_name')

    # Get pending benefit requests to display as notifications/action items
    pending_benefits = Benefit.objects.filter(status='Pending').select_related('member').order_by('-pk')

    # Get announcements the user hasn't read
    unread_announcements = Announcement.objects.exclude(read_by=request.user)

    context = {
        'navbar':True,
        'total_fund_balance': total_fund_balance,
        'total_members': total_members,
        'recent_activities': recent_activities,
        'outstanding_members': outstanding_members,
        'current_month_year': current_month_year,
        'yearly_total_contributions': yearly_total_contributions,
        'monthly_total_contributions': monthly_total_contributions,
        'pending_benefits': pending_benefits,
        'unread_announcements': unread_announcements,
    }
    return render(request, 'finance/dashboard.html', context)


@login_required
def manageBenefitsView(request):
    """
    Displays a list of all benefit requests for the finance team to manage.
    Allows filtering by status.
    """
    status_filter = request.GET.get('status', 'Pending')
    if status_filter not in ['Pending', 'Approved', 'Denied']:
        status_filter = 'Pending'

    benefit_requests = Benefit.objects.filter(status=status_filter).select_related('member').order_by('-date_submitted')

    context = {
        'navbar': True,
        'benefit_requests': benefit_requests,
        'status_filter': status_filter,
    }
    return render(request, 'finance/manage_benefits.html', context)


@login_required
@require_POST
def processBenefitView(request, pk, action):
    """
    Processes a benefit request by approving or denying it.
    """
    benefit = get_object_or_404(Benefit, pk=pk)
    
    if benefit.status == 'Pending':
        if action == 'approve':
            benefit.status = 'Approved'
            messages.success(request, f"Benefit request for {benefit.member.get_full_name()} has been approved.")
        elif action == 'deny':
            benefit.status = 'Denied'
            messages.warning(request, f"Benefit request for {benefit.member.get_full_name()} has been denied.")
        
        # Record who processed the request and when
        benefit.processed_by = request.user
        benefit.processed_date = timezone.now()
        benefit.save()
    else:
        messages.error(request, "This request has already been processed and cannot be changed.")

    # Redirect back to the pending list, which is the most common workflow.
    return redirect(f"{reverse('finance:manage_benefits')}?status=Pending")


@login_required
def honourBenefitView(request, pk):
    """
    Marks a benefit as honoured after confirming/entering the amount.
    """
    benefit = get_object_or_404(Benefit, pk=pk)
    
    if benefit.status != 'Approved' or benefit.honoured:
        messages.error(request, "Only approved, un-honoured benefits can be processed.")
        return redirect(f"{reverse('finance:manage_benefits')}?status=Approved")

    if request.method == 'POST':
        form = HonourBenefitForm(request.POST, instance=benefit)
        if form.is_valid():
            honoured_benefit = form.save(commit=False)
            honoured_benefit.honoured = True
            honoured_benefit.processed_date = timezone.now()
            honoured_benefit.save()
            messages.success(request, f"Benefit for {benefit.member.get_full_name()} has been marked as honoured with an amount of GH₵ {honoured_benefit.amount:,.2f}.")

            # Send SMS notification
            member = honoured_benefit.member
            if member.phone_number:
                message = f"Dear {member.get_full_name()}, your benefit of GHC{honoured_benefit.amount} has been honoured. Thank you."
                send_sms(member.phone_number, message)

            return redirect(f"{reverse('finance:manage_benefits')}?status=Approved")
        else:
            messages.error(request, "Please correct the amount.")
    else:
        form = HonourBenefitForm(instance=benefit)

    context = {
        'navbar': True,
        'form': form,
        'benefit': benefit,
    }
    return render(request, 'finance/honour_benefit.html', context)

@login_required
def financeReportView(request):
    """
    Provides a detailed financial report with year-based filtering.
    """
    today = timezone.now().date()
    
    # Determine the year to display. Default to the current year.
    try:
        selected_year = int(request.GET.get('year', today.year))
    except (ValueError, TypeError):
        selected_year = today.year

    # Get a list of all years for which payments exist, for the filter dropdown.
    payment_dates = Dues.objects.dates('payment_date', 'year', order='DESC')
    available_years = [date.year for date in payment_dates]

    # Filter dues for the selected year
    dues_for_year = Dues.objects.filter(payment_date__year=selected_year)

    # --- Key Metrics ---
    total_fund_balance = Dues.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    yearly_total_contributions = dues_for_year.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_members = CustomUser.objects.filter(is_superuser=False, is_active=True).count()
    
    # Calculate average contribution per member for the year
    average_contribution = (yearly_total_contributions / total_members) if total_members > 0 else Decimal('0.00')

    # --- Monthly Breakdown ---
    # Group contributions by month for the selected year
    monthly_breakdown = dues_for_year.annotate(
        month=TruncMonth('payment_date')
    ).values(
        'month'
    ).annotate(
        total=Sum('amount')
    ).order_by('month')

    # --- Top Contributors ---
    # Get the top 10 contributors for the selected year
    top_contributors = dues_for_year.values(
        'member__id', 
    ).annotate(
        full_name=Concat('member__first_name', Value(' '), 'member__last_name'),
        total_paid=Sum('amount')
    ).order_by('-total_paid')[:10]

    # Net financial position for the year
    net_for_year = yearly_total_contributions

    context = {
        'navbar': True,
        'selected_year': selected_year,
        'available_years': available_years,
        'total_fund_balance': total_fund_balance,
        'yearly_total_contributions': yearly_total_contributions,
        'average_contribution': average_contribution,
        'monthly_breakdown': monthly_breakdown,
        'top_contributors': top_contributors,
        'net_for_year': net_for_year,
    }
    return render(request, 'finance/finance_report.html', context)


@login_required
def financeMembersListView(request):
    # Filter out superusers from the list, as they are not regular members
    # and do not have dues payment history. This prevents confusion.
    members_list = CustomUser.objects.filter(is_superuser=False, is_active=True).order_by('first_name', 'last_name')

    search_query = request.GET.get("q")
    if search_query:
        members_list = members_list.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(
            Q(full_name__icontains=search_query) | Q(staff_id__icontains=search_query)
        )

    paginator = Paginator(members_list, 15)  # Show 15 members per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'navbar': True,
        'search_query': search_query or "",
    }
    return render(request, 'finance/members_list.html', context)


@login_required
def financeMemberDetailView(request, pk):
    member = get_object_or_404(CustomUser, pk=pk)
    # Define the maximum amount that can be recorded for a single month.
    MAX_MONTHLY_PAYMENT = Decimal('10.00')

    if request.method == 'POST':
        form = DuesPaymentForm(request.POST)
        if form.is_valid():
            total_amount_paid = form.cleaned_data['amount']
            payment_date = form.cleaned_data['payment_date']
            notes = form.cleaned_data['notes']

            # 1. Check for existing payments in the selected month to "top-up" first.
            existing_payment_for_month = Dues.objects.filter(
                member=member,
                payment_date__year=payment_date.year,
                payment_date__month=payment_date.month
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            # 2. Calculate how much more can be paid for the selected month.
            room_in_month = max(Decimal('0.00'), MAX_MONTHLY_PAYMENT - existing_payment_for_month)

            # 3. Determine the amount to apply to the selected month.
            amount_for_selected_month = min(total_amount_paid, room_in_month)

            # 4. If there's room, create the payment record for the selected month.
            if amount_for_selected_month > 0:
                Dues.objects.create(
                    member=member,
                    amount=amount_for_selected_month,
                    payment_date=payment_date,
                    notes=notes
                )

            # 5. Calculate the remaining amount to be spread to future months.
            remaining_amount = total_amount_paid - amount_for_selected_month
            current_date = payment_date

            # 6. Loop and create new Dues records for subsequent months until the entire amount is allocated.
            while remaining_amount > 0:
                # A reliable way to get the first day of the next month.
                current_date = current_date.replace(day=1) + datetime.timedelta(days=32)
                next_month_date = current_date.replace(day=1)

                # The amount for this future payment is the lesser of the remaining balance or the monthly max.
                amount_for_this_month = min(remaining_amount, MAX_MONTHLY_PAYMENT)
                Dues.objects.create(
                    member=member,
                    amount=amount_for_this_month,
                    payment_date=next_month_date,
                    notes=f"Carried over from payment on {payment_date.strftime('%Y-%m-%d')}"
                )
                remaining_amount -= amount_for_this_month
                current_date = next_month_date

            messages.success(request, f"Dues payment for {member.get_full_name()} recorded and spread across future months.")
            return redirect('finance:finance_member_detail', pk=member.pk)
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        form = DuesPaymentForm()

    # Base queryset for all dues related to the member
    all_dues_history = member.dues.all().order_by('-payment_date')

    # Get unique years for which payments exist, for the filter buttons
    # The .dates() method returns a list of datetime.date objects. We extract the year from each.
    payment_dates = all_dues_history.dates('payment_date', 'year', order='DESC')
    available_years = [date.year for date in payment_dates]

    # Get the selected year from the URL query parameter for filtering
    selected_year_str = request.GET.get('year')
    dues_for_display = all_dues_history
    selected_year = None

    if selected_year_str and selected_year_str.isdigit():
        selected_year = int(selected_year_str)
        dues_for_display = all_dues_history.filter(payment_date__year=selected_year)

    # Calculate the total for the displayed period (before pagination) and the grand total
    total_dues = dues_for_display.aggregate(total=Sum('amount'))['total'] or 0.00
    grand_total_dues = all_dues_history.aggregate(total=Sum('amount'))['total'] or 0.00

    # Add pagination to the dues history
    paginator = Paginator(dues_for_display, 15)  # Show 15 payments per page
    page_number = request.GET.get('page')
    dues_page_obj = paginator.get_page(page_number)

    context = {
        'navbar': True,
        'member': member,
        # Pass the paginated object to the template
        'dues_history': dues_page_obj,
        'total_dues': total_dues,
        'grand_total_dues': grand_total_dues,
        'form': form,
        'available_years': available_years,
        'selected_year': selected_year,
    }
    return render(request, 'finance/member_detail.html', context)


@login_required
def financeMemberStatementPrintView(request, pk):
    member = get_object_or_404(CustomUser, pk=pk)
    dues_history = member.dues.all().order_by('payment_date')
    total_dues = dues_history.aggregate(total=Sum('amount'))['total'] or 0.00
    context = {
        'member': member,
        'dues_history': dues_history,
        'total_dues': total_dues,
        'current_date': timezone.now(),
    }
    return render(request, 'finance/member_statement_print.html', context)


@login_required
def dues_edit_view(request, pk):
    """
    View to edit an existing dues payment.
    Note: This view performs a simple update on a single record. It does not
    re-run the complex payment-spreading logic from the detail view.
    """
    due = get_object_or_404(Dues, pk=pk)
    member = due.member
    if request.method == 'POST':
        form = DuesPaymentForm(request.POST, instance=due)
        if form.is_valid():
            form.save()
            messages.success(request, "Dues payment updated successfully.")
            return redirect('finance:finance_member_detail', pk=member.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DuesPaymentForm(instance=due)

    context = {'form': form, 'member': member, 'navbar': True}
    return render(request, 'finance/dues_edit.html', context)


@login_required
def dues_delete_view(request, pk):
    """
    View to delete a dues payment after confirmation.
    """
    due = get_object_or_404(Dues, pk=pk)
    if request.method == 'POST':
        due.delete()
        messages.success(request, "Dues payment has been deleted.")
        return redirect('finance:finance_member_detail', pk=due.member.pk)

    context = {'due': due, 'member': due.member, 'navbar': True}
    return render(request, 'finance/dues_confirm_delete.html', context)