from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max, Value, Q, Count
from django.db.models.functions import Concat, TruncMonth
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages

from accounts.models import CustomUser
from finance.models import Dues
from members.models import Benefit
from secretary.models import Announcement


@login_required
def chairDashboardView(request):
    """
    Displays the main dashboard for the chairperson, providing a comprehensive
    overview of the association's key metrics.
    """
    today = timezone.now().date()

    # --- Financial Metrics ---
    total_fund_balance = Dues.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    yearly_total_contributions = Dues.objects.filter(
        payment_date__year=today.year
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    monthly_total_contributions = Dues.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # --- Benefit Metrics ---
    honoured_benefits = Benefit.objects.filter(honoured=True)
    total_benefit_amount = honoured_benefits.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    honoured_benefits_count = honoured_benefits.count()
    benefited_members_count = honoured_benefits.values('member').distinct().count()
    # The balance difference between total funds collected and total benefits paid out.
    balance_after_benefits = total_fund_balance - total_benefit_amount

    # --- Member Metrics ---
    total_members = CustomUser.objects.filter(is_superuser=False, is_active=True).count()
    current_month_year = today.strftime('%B %Y')
    paid_this_month_ids = Dues.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).values_list('member_id', flat=True).distinct()
    outstanding_members = CustomUser.objects.filter(
        is_superuser=False, is_active=True
    ).exclude(
        pk__in=paid_this_month_ids
    ).order_by('last_name', 'first_name')

    # --- Actionable Items ---
    pending_benefits = Benefit.objects.filter(status='Pending').select_related('member').order_by('-pk')
    unread_announcements = Announcement.objects.exclude(read_by=request.user)

    context = {
        'navbar': True,
        'total_fund_balance': total_fund_balance,
        'total_members': total_members,
        'yearly_total_contributions': yearly_total_contributions,
        'monthly_total_contributions': monthly_total_contributions,
        'outstanding_members': outstanding_members,
        'current_month_year': current_month_year,
        'pending_benefits': pending_benefits,
        'total_benefit_amount': total_benefit_amount,
        'honoured_benefits_count': honoured_benefits_count,
        'benefited_members_count': benefited_members_count,
        'balance_after_benefits': balance_after_benefits,
        'unread_announcements': unread_announcements,
    }
    return render(request, 'chair/dashboard.html', context)


@login_required
def membersListView(request):
    """
    Displays a list of all members for the chairperson.
    """
    query = request.GET.get('q')
    members_list = CustomUser.objects.filter(is_superuser=False, is_active=True).order_by('first_name', 'last_name')

    if query:
        members_list = members_list.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(staff_id__icontains=query)
        ).distinct()

    context = {
        'navbar': True,
        'members_list': members_list,
    }
    return render(request, 'chair/members_list.html', context)


@login_required
def manageBenefitsView(request):
    """
    Allows the chairperson to view and manage benefit requests, filtering by status.
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
    return render(request, 'chair/manage_benefits.html', context)


@login_required
@require_POST
def processBenefitView(request, pk, action):
    """
    Handles the logic for approving or denying a benefit request.
    """
    benefit = get_object_or_404(Benefit, pk=pk)

    if benefit.status == 'Pending':
        if action == 'approve':
            benefit.status = 'Approved'
            messages.success(request, f"Benefit request for {benefit.member.get_full_name()} has been approved.")
        elif action == 'deny':
            benefit.status = 'Denied'
            messages.warning(request, f"Benefit request for {benefit.member.get_full_name()} has been denied.")
        benefit.save()
    else:
        messages.error(request, "This request has already been processed.")

    return redirect('chairperson:manage_benefits')


@login_required
def memberDetailView(request, pk):
    """
    Displays a detailed view of a member for the chairperson, including
    their payment history.
    """
    member = get_object_or_404(CustomUser, pk=pk)
    dues_history = Dues.objects.filter(member=member).order_by('-payment_date')
    total_dues = dues_history.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    context = {
        'navbar': True,
        'member': member,
        'dues_history': dues_history,
        'total_dues': total_dues,
    }
    return render(request, 'chair/member_detail.html', context)


@login_required
def chairpersonMemberStatementPrintView(request, pk):
    """
    Generates a printable financial statement for a specific member,
    intended for the chairperson's use.
    """
    member = get_object_or_404(CustomUser, pk=pk)
    dues_history = Dues.objects.filter(member=member).order_by('-payment_date')
    total_dues = dues_history.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    context = {
        'navbar': False,  # Use a minimal layout for printing
        'member': member,
        'dues_history': dues_history,
        'total_dues': total_dues,
    }
    return render(request, 'chair/member_statement_print.html', context)


@login_required
@require_POST
def dismissAnnouncementView(request, pk):
    """
    Marks an announcement as read by the current user.
    """
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.read_by.add(request.user)
    return redirect('chairperson:chairperson_dashboard')


@login_required
def financialReportView(request):
    """
    Provides a detailed financial report for the chairperson with year-based filtering.
    """
    today = timezone.now().date()

    try:
        selected_year = int(request.GET.get('year', today.year))
    except (ValueError, TypeError):
        selected_year = today.year

    payment_dates = Dues.objects.dates('payment_date', 'year', order='DESC')
    available_years = [date.year for date in payment_dates]
    # Ensure the selected year is in the list, especially for the current year
    # if no payments have been made yet.
    if selected_year not in available_years:
        available_years.append(selected_year)
        available_years.sort(reverse=True)

    dues_for_year = Dues.objects.filter(payment_date__year=selected_year)

    total_fund_balance = Dues.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    yearly_total_contributions = dues_for_year.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    total_members = CustomUser.objects.filter(is_superuser=False, is_active=True).count()
    average_contribution = (yearly_total_contributions / total_members) if total_members > 0 else Decimal('0.00')

    monthly_breakdown = dues_for_year.annotate(
        month=TruncMonth('payment_date')
    ).values('month').annotate(total=Sum('amount')).order_by('month')

    top_contributors = dues_for_year.values(
        'member__id',
    ).annotate(
        full_name=Concat('member__first_name', Value(' '), 'member__last_name'),
        total_paid=Sum('amount')
    ).order_by('-total_paid')[:10]

    # --- Benefit Metrics ---
    benefits_for_year = Benefit.objects.filter(date_submitted__year=selected_year)
    total_benefits = benefits_for_year.count()
    pending_benefits = benefits_for_year.filter(status='Pending').count()
    approved_benefits = benefits_for_year.filter(status='Approved').count()
    denied_benefits = benefits_for_year.filter(status='Denied').count()
    honoured_benefits = benefits_for_year.filter(honoured=True).count()
    total_amount_honoured = benefits_for_year.filter(honoured=True).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    balance_after_benefits = total_fund_balance - total_amount_honoured


    context = {
        'navbar': True,
        'selected_year': selected_year,
        'available_years': available_years,
        'total_fund_balance': total_fund_balance,
        'yearly_total_contributions': yearly_total_contributions,
        'total_members': total_members,
        'average_contribution': average_contribution,
        'monthly_breakdown': monthly_breakdown,
        'top_contributors': top_contributors,
        'total_benefits': total_benefits,
        'pending_benefits': pending_benefits,
        'approved_benefits': approved_benefits,
        'denied_benefits': denied_benefits,
        'honoured_benefits': honoured_benefits,
        'total_amount_honoured': total_amount_honoured,
        'balance_after_benefits': balance_after_benefits,
    }
    return render(request, 'chair/financial_report.html', context)
