from django.shortcuts import render
from django.core.management import execute_from_command_line

def home(request):
    return render(request, 'home.html')

def upload_form(request):
    return render(request, 'upload_form.html')

def run():
    # Run the migrations
    execute_from_command_line(['manage.py', 'migrate', '--settings=cenas1.settings'])

    # Start the Django development server
    execute_from_command_line(['manage.py', 'runserver', '--settings=cenas1.settings'])
