from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def upload_form(request):
    return render(request, 'upload_form.html')