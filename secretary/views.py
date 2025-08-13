from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.forms import EditUserForm
from .models import Announcement
from django.http import HttpResponseForbidden
from .forms import AnnouncementForm

# Create your views here.
@login_required
def secretaryDashboardView(request):
    """
    Displays the secretary dashboard with recent announcements and a form to add new ones.
    """
    announcements = Announcement.objects.all()[:5]  # Get the 5 most recent announcements
    context = {
        'navbar': True,
        'announcements': announcements,
    }
    return render(request, 'secretary/dashboard.html', context)

@login_required
def membersListView(request):
    """
    Provides a paginated list of all users for the secretary, with search functionality.
    """
    query = request.GET.get('q', '')
    # Start with the base queryset
    members_list = CustomUser.objects.all()

    if query:
        members_list = members_list.filter(
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).distinct()

    # Order the results for consistent display before pagination
    members_list = members_list.order_by('first_name', 'last_name')

    # Set up pagination: 15 members per page
    paginator = Paginator(members_list, 15)
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)

    context = {
        'members': members,
        'query': query,
    }
    return render(request, 'secretary/members_list.html', context)

@login_required
def memberDetailView(request, pk):
    """
    Displays the details for a specific member.
    """
    member = get_object_or_404(CustomUser, pk=pk)
    context = {
        'member': member,
    }
    return render(request, 'secretary/member_detail.html', context)

@login_required
def memberEditView(request, pk):
    """
    Handles editing of a member's details by a secretary.
    """
    member = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"Details for {member.get_full_name()} updated successfully.")
            return redirect('member_detail', pk=member.pk)
    else:
        form = EditUserForm(instance=member)

    context = {
        'form': form,
        'member': member,
    }
    return render(request, 'secretary/member_edit_form.html', context)

@login_required
def announcement_add_view(request):
    """
    Handles creating a new announcement on a dedicated page.
    """
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            messages.success(request, "Announcement posted successfully.")
            return redirect('secretary_dashboard')
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        form = AnnouncementForm()

    context = {
        'form': form,
    }
    return render(request, 'secretary/announcement_form.html', context)

@login_required
def announcement_edit_view(request, pk):
    """
    Handles editing an existing announcement.
    """
    announcement = get_object_or_404(Announcement, pk=pk)

    # Check if the current user is the author of the announcement
    if announcement.author != request.user:
        return HttpResponseForbidden("You are not authorized to edit this announcement.")

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully.")
            return redirect('secretary_dashboard')
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        form = AnnouncementForm(instance=announcement)

    context = {
        'form': form,
        'announcement': announcement,
    }
    return render(request, 'secretary/announcement_edit_form.html', context)

@login_required
def announcement_delete_view(request, pk):
     """
     Handles deleting an existing announcement.
     """
     announcement = get_object_or_404(Announcement, pk=pk)

     # Check if the current user is the author of the announcement
     if announcement.author != request.user:
         return HttpResponseForbidden("You are not authorized to delete this announcement.")

     if request.method == 'POST':
         announcement.delete()
         messages.success(request, "Announcement deleted successfully.")
         return redirect('secretary_dashboard')

     context = {
         'announcement': announcement,
     }
     return render(request, 'secretary/announcement_delete_confirm.html', context)

@login_required
def dismiss_announcement_view(request, pk):
    """
    Marks an announcement as read for the current user and redirects them back
    to the page they came from.
    """
    # Determine a sensible fallback redirect based on user type.
    if hasattr(request.user, 'is_staff') and request.user.is_staff:
        fallback_redirect = 'finance:finance_dashboard'
    else:
        fallback_redirect = 'dashboard' # Assumes 'dashboard' is the member dashboard URL name.

    if request.method == 'POST':
        announcement = get_object_or_404(Announcement, pk=pk)
        announcement.read_by.add(request.user)

    # Redirect back to the referer page, or to the fallback if not available.
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer or fallback_redirect)