from django.shortcuts import render

# Create your views here.
def homepage(request):

    return render(request, 'general/index.html', {'navbar':True})

def about_page(request):
    return render(request, 'general/about.html', {'navbar': True})

def contact_page(request):
    return render(request, 'general/contact.html', {'navbar': True})

def constitution_page(request):
    return render(request, 'general/constitution.html', {'navbar': True})