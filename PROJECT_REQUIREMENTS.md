# Campus Supply Project Requirements and Teacher Setup

This guide explains how to run and assess the Django semester project on a separate computer, including database creation, sample data, and administrator access.

Repository: [IAP Semester Project](https://github.com/lam-hurman21/IAP-SEMESTER-PROJECT)

## 1 Software requirements

| Requirement | Details |
| --- | --- |
| Python | Python 3.10 or later compatible with Django 5.2; tested with Python 3.13.3 |
| Django | `Django>=5.2,<5.3`, installed from `requirements.txt`; tested with Django 5.2.19 |
| Git | Required to clone the repository; alternatively download and extract its ZIP from GitHub |
| Database | SQLite, included with Python; no separate database server is required |
| Browser | A modern browser with cookies enabled for authentication and sessions |
| Internet | Needed to download the project and install Django; the app then runs locally |
| Terminal | Windows PowerShell for the commands below; macOS and Linux alternatives are also included |

VS Code is optional. Node.js and npm are not required.

## 2 Download the project

Run these commands in the folder where you want to keep the project:

```powershell
git clone https://github.com/lam-hurman21/IAP-SEMESTER-PROJECT.git
cd IAP-SEMESTER-PROJECT
```

If you downloaded a ZIP instead, extract it and open a terminal in the folder containing `manage.py` and `requirements.txt`.

## 3 Set up Python and the database

Run from the project folder in Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_catalog
```

These commands create a virtual environment, install Django, create the database tables, and add three sample products: A5 Notebook, Everyday Backpack, and Desk Lamp. The sample-data command can be repeated without replacing existing products or edits.

The SQLite database is created as `db.sqlite3` in the project folder. It contains the categories, products, user accounts, permissions, sessions, and admin logs. The database and virtual environment are excluded from Git. Migration files are included, so every fresh clone must run `migrate` and create its own admin account.

The commands use the virtual environment's interpreter directly, so activating the environment or changing PowerShell execution policy is unnecessary.

## 4 Create the teacher admin account

Use these credentials for local project assessment:

| Field | Value |
| --- | --- |
| Username | `Lameck` |
| Password | `fYFPbwzcVpDvnWreLuJe` |
| Role | Superuser with access to all administration features |

**The account is not created automatically by cloning the repository.** After running the migrations, create it in PowerShell using:

```powershell
$env:DJANGO_SUPERUSER_PASSWORD = 'fYFPbwzcVpDvnWreLuJe'
.\.venv\Scripts\python.exe manage.py createsuperuser --noinput --username Lameck --email teacher@example.com
Remove-Item Env:DJANGO_SUPERUSER_PASSWORD
```

`teacher@example.com` is a placeholder and may be replaced with the teacher's email address. Log in using the username, not the email address. The username and password are case-sensitive.

If the account already exists, skip its creation. If its password was changed, reset it with:

```powershell
.\.venv\Scripts\python.exe manage.py changepassword Lameck
```

Enter the documented password twice to restore these assessment credentials, or choose a new password. Password input is hidden while typing. A user registered through the public registration page is a member and does not have admin access.

## 5 Start the whole project

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8010
```

Keep this terminal running while using the website. Press `Ctrl+C` to stop the server. Django serves the pages and local static assets; no separate frontend server is required.

| Page | Local address |
| --- | --- |
| Catalog | http://127.0.0.1:8010/ |
| About | http://127.0.0.1:8010/about/ |
| Registration | http://127.0.0.1:8010/accounts/register/ |
| Login | http://127.0.0.1:8010/accounts/login/ |
| Account profile | http://127.0.0.1:8010/accounts/profile/ |
| Administration | http://127.0.0.1:8010/admin/ |
| Add product | http://127.0.0.1:8010/products/new/ |

These addresses work on the computer running the server. To assess the admin features, open `/admin/` and use the credentials in section 4.

## 6 Features to assess

| Area | Implemented behavior |
| --- | --- |
| URLs and views | App routes are included by the project URL configuration; views render pages and process forms |
| Templates | Shared base layout, app-level product templates, and project-level about and account templates |
| Models | Category and Product models with relationships, publication status, creator, and timestamps |
| Forms | Validated registration, login, and product ModelForm with error display and CSRF protection |
| Authentication | Registration, login, POST logout, password hashing, and protected account pages |
| Sessions | Database-backed sessions; browser-length login by default and a 14-day remember-me option |
| Admin | Category and product management, user and group management, search, filters, and creator tracking |
| Permissions | Product creation and editing require staff status and the relevant Django permissions; superusers have full access |
| Catalog | Loads products from SQLite and hides inactive products from public visitors |

Suggested assessment sequence:

1. Open the catalog and About page and confirm that navigation and images work.
2. Register a member account, open the profile, log out, and log back in with remember-me selected.
3. Log out of the member account and sign in to the admin panel as `Lameck`.
4. Add a category, then create or edit a product in the admin panel or through the product form.
5. Mark a product inactive and confirm that it is hidden when viewing the catalog after logging out.

Products accept local static image paths such as `products/notebook.jpg`. Image uploading, checkout, and payment processing are outside the current implementation.

## 7 Run the checks and tests

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py migrate --check
.\.venv\Scripts\python.exe manage.py test products --verbosity 2
```

Expected results: no Django system-check errors, no model changes needing migrations, no unapplied migrations, and all 22 tests passing. Tests use a separate temporary database and do not replace the assessment database.

## 8 macOS and Linux commands

After cloning the repository and changing into its folder, use these commands instead of the PowerShell setup commands:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py seed_catalog
DJANGO_SUPERUSER_PASSWORD='fYFPbwzcVpDvnWreLuJe' \
  ./.venv/bin/python manage.py createsuperuser --noinput \
  --username Lameck --email teacher@example.com
./.venv/bin/python manage.py runserver 127.0.0.1:8010
```

For the checks, tests, or password reset, replace `.\.venv\Scripts\python.exe` with `./.venv/bin/python`.

## 9 Troubleshooting

| Problem | Solution |
| --- | --- |
| `py` is not recognized | Install Python, reopen the terminal, or use `python -m venv .venv` if `python --version` reports a supported version |
| `No module named django` | Install `requirements.txt` using the virtual environment interpreter shown in section 3 |
| `no such table` or unapplied migrations | Run `manage.py migrate` with the virtual environment interpreter |
| Empty catalog | Run `manage.py seed_catalog` or add categories and products in admin |
| Admin login rejected | Create the account as described in section 4, verify exact capitalization, or use `changepassword Lameck` |
| Username already taken during setup | The account exists; skip account creation or reset its password |
| Port is in use or access is denied | Start on another port, for example `127.0.0.1:8011`, and use that port in all browser addresses |
| Browser cannot connect | Keep the server terminal open and check that the browser address matches its printed address |

The supplied configuration is for local coursework assessment. The setup commands recreate the database and credentials without including `db.sqlite3` or `.venv` in the repository.
