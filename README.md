# Django Semester Project

Starter lab for Application Programming for the Internet, following the Django Project Setup practical manual. The sample project is Campus Supply, a small student-essentials catalog.

Tested with Python 3.13 and Django 5.2 LTS. Product entries are sample data in the view, not database-backed inventory or a live store.

## Start the Existing Lab

Open a PowerShell terminal in this project folder:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Open http://127.0.0.1:8000/. The second page is http://127.0.0.1:8000/about/.

If the server is already running, use the existing server or choose another port, such as `8001`. Stop the server with `Ctrl+C` before starting another server on the same port.

VS Code is configured to use the local virtual environment. With the Python and Python Debugger extensions installed, select **Django: runserver** and press `F5` to debug. Stop any server already using port 8000 first.

## Set Up a Fresh Clone

Install Python 3.10 or later and Git, then run these commands from the cloned project folder:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

To activate the environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

The explicit interpreter commands above also work without activation and do not require changing PowerShell's execution policy.

## Lab Structure

```text
config/                          Django project configuration
products/                        Registered Django app
    urls.py                      App URL patterns
    views.py                     Catalog and about views
    tests.py                     URL, template, and navigation tests
    templates/products/index.html  App-level template
    static/products/             Styles and local product images
    migrations/                  App migration package
templates/
    base.html                    Shared project-level layout
    about.html                   Project-level page template
.vscode/                         Interpreter and debug settings
manage.py                        Django management commands
requirements.txt                 Django dependency
.gitignore                       Local environment/database exclusions
```

The app is registered in [config/settings.py](config/settings.py), which also adds the project-level template directory. [config/urls.py](config/urls.py) includes [products/urls.py](products/urls.py).

The `/` view renders [products/templates/products/index.html](products/templates/products/index.html). The `/about/` view renders [templates/about.html](templates/about.html). Both extend [templates/base.html](templates/base.html).

## Verify the Lab

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test products --verbosity 2
.\.venv\Scripts\python.exe manage.py migrate --check
```

The three tests check both template locations, sample catalog content, and navigation between the pages. Visit both URLs in a browser to check their layout and images.

The default Django admin is available at http://127.0.0.1:8000/admin/. No administrator account is created automatically. To create your own account, enter its details directly in your terminal:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## GitHub Submission

Submit https://github.com/lam-hurman21/IAP-SEMESTER-PROJECT. The localhost development-server URL is not a submission link.

The Git remote `origin` points to `https://github.com/lam-hurman21/IAP-SEMESTER-PROJECT.git`. To commit and push future changes:

```powershell
git add .
git commit -m "Update semester project"
git push
```

Authenticate directly in your terminal or browser if Git requests it; never put passwords or access tokens in project files or chat.

Before submitting, confirm the repository is accessible to your instructor and contains the project, app, and at least one commit. [.gitignore](.gitignore) excludes the virtual environment, SQLite database, Python caches, and local environment files.

## Development Settings

This is a local lab, not a production deployment: `DEBUG` is enabled and the default secret key is deliberately development-only. Set `DJANGO_SECRET_KEY` in the process environment to override it. Environment files are ignored by Git but are not loaded automatically.

Before deployment, configure a private secret key, disable debug mode, configure allowed hosts, and follow the [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

## Image Sources

Sample images are stored locally and come from Unsplash: [notebook](https://images.unsplash.com/photo-1531346878377-a5be20888e57), [backpack](https://images.unsplash.com/photo-1553062407-98eeb64c6a62), and [lamp](https://images.unsplash.com/photo-1507473885765-e6ed057f782c). See the [Unsplash license](https://unsplash.com/license).