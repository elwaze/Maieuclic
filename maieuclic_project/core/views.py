from django.shortcuts import render

# Create your views here.


# home
def home(request):
    return render(request, 'home.html')


# legal notices
def legal_notices(request):
    return render(request, 'legal_notices.html')


# legal notices
def contact(request):
    return render(request, 'contact.html')
