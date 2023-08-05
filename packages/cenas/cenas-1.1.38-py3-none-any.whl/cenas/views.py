import os
import sys
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
application = get_wsgi_application()

def home(request):
    return render(request, 'home.html')

def upload_form(request):
    return render(request, 'upload_form.html')

def run():
    # Change to the project's root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    # Add the local bin directory to PATH
    home_dir = os.path.expanduser("~")
    bin_dir = os.path.join(home_dir, ".local", "bin")
    os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"

    # Run the migrations
    execute_from_command_line(['manage.py', 'migrate', '--settings=cenas1.settings'])

    # Start the Django development server
    execute_from_command_line(['manage.py', 'runserver', '--settings=cenas1.settings'])

if __name__ == '__main__':
    run()
