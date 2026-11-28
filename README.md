# Campus Supply — Django Semester Project

A student-essentials catalog built with Python and Django 5.2 LTS. Products and categories are stored in SQLite. The app includes Django forms, registration, login/logout, database-backed sessions, and an administration panel.

For teacher assessment, see [Project requirements and teacher setup](PROJECT_REQUIREMENTS.md), including software requirements, complete setup commands, and admin credentials with account-creation instructions.

## Set up and run

From PowerShell in this project directory:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_catalog
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Use Python 3.10 or later. If `.venv` already exists, skip creating it. Enter your own administrator credentials in the terminal when prompted, or follow the [teacher setup guide](PROJECT_REQUIREMENTS.md#4-create-the-teacher-admin-account) to create the documented assessment account. Admin accounts are not created automatically.

`seed_catalog` is optional: it adds the original three sample products and their categories. Running it again preserves existing entries and edits. Without sample data, the catalog shows an empty-state message until products are added.

## Pages and access

| URL | Purpose | Access |
| --- | --- | --- |
| `/` | Database-backed product catalog | Public; inactive products visible only to staff with product view permission |
| `/about/` | About Campus Supply | Public |
| `/accounts/register/` | Registration form | Visitors; signs in the new member |
| `/accounts/login/` | Login form with remember-me option | Visitors |
| `/accounts/logout/` | Logout | POST with CSRF token; use the navigation button |
| `/accounts/profile/` | Account details and session policy | Signed-in users |
| `/products/new/` | Product ModelForm | Staff with add-product permission |
| `/products/<id>/edit/` | Edit product ModelForm | Staff with change-product permission |
| `/admin/` | Django administration | Active staff; model permissions determine access |

The administrator created with `createsuperuser` has all permissions. For another catalog manager, use **Admin → Users**, enable **Staff status**, and grant the appropriate product/category view, add, change, and delete permissions directly or through a group. Staff status alone does not grant product editing access. Members registering on the website receive no staff privileges.

## Implementation

- **Models:** `Category` has a unique name. `Product` belongs to a category and stores its description, optional static image path/alternative text, publication status, creator, and timestamps. Categories containing products cannot be deleted; deleting a creator preserves their products. The initial migration is included.
- **Forms:** `RegistrationForm` uses Django password validation and requires an email address. `LoginForm` adds remember-me to Django authentication. `ProductForm` validates catalog entries and excludes creator and timestamp fields. Forms render errors and include CSRF protection.
- **Authentication and sessions:** Django hashes passwords and stores authenticated sessions in the database. Registration and normal login use browser-length sessions; remember-me lasts up to 14 days. Browser session restoration may retain a browser-length session. Logout clears the session. Protected pages redirect visitors to login; login accepts safe local `next` destinations.
- **Admin:** Categories and products support search, product filters, category autocomplete, and automatic creator assignment. Creator and timestamps are read-only. Standard Django user/group administration is available.

Product images use paths under `products/static/`, such as `products/notebook.jpg`; this is not an image-upload feature. Categories can be added in the administration panel before creating products.

## Verification

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test products --verbosity 2
.\.venv\Scripts\python.exe manage.py migrate --check
```

Tests cover database catalog rendering, relationships, repeatable sample data, form validation, registration, password hashing, login redirects, session expiry, logout, CSRF protection, staff permissions, product management, and admin access. Tests use a separate test database.

VS Code is configured for the local virtual environment. With the Python and Python Debugger extensions installed, select **Django: runserver** and press `F5`. Stop any server already using port 8000 first, or choose another port.

## Development settings

This is a local development project. `DEBUG` is enabled and the default secret key is development-only. Set `DJANGO_SECRET_KEY` in the process environment to override it. Environment files are ignored by Git and are not loaded automatically. Before deployment, configure a private key, disable debug mode, configure allowed hosts and HTTPS cookies, and follow the [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

The virtual environment, local SQLite database, Python caches, and local environment files are excluded from Git. Commit migrations along with model changes. To remove expired session records periodically, run `manage.py clearsessions`.

## Repository and image sources

Submit the [GitHub repository](https://github.com/lam-hurman21/IAP-SEMESTER-PROJECT), not a localhost URL. No commits or pushes happen automatically.

Sample images are stored locally and come from Unsplash: [notebook](https://images.unsplash.com/photo-1531346878377-a5be20888e57), [backpack](https://images.unsplash.com/photo-1553062407-98eeb64c6a62), and [lamp](https://images.unsplash.com/photo-1507473885765-e6ed057f782c). See the [Unsplash license](https://unsplash.com/license).
