import os
import site

# Get the user-site directory
user_site = site.getusersitepackages()

# Add the user-site bin directory to the PATH
bin_dir = os.path.join(user_site, 'bin')
with open(os.path.join(user_site, 'sitecustomize.py'), 'w') as f:
    f.write(f'import os; os.environ["PATH"] += os.pathsep + "{bin_dir}"\n')