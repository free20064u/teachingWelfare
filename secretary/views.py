from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.forms import EditUserForm

# Create your views here.
@login_required
def secretaryDashboardView(request):
    context = {
        'navbar': True,
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