# Absolute Icecream

Premium direct-to-consumer ice cream storefront built with Flask.

## Technology

- Python 3.10+
- Flask, Jinja2, SQLAlchemy, and Flask-Migrate
- SQLite for local development; PostgreSQL is supported for deployment
- Redis and Celery for background tasks
- HTML, CSS, and JavaScript

## Local development

### Requirements

Install Git and Python 3.10 or later. On Windows, install Python with the
Python Launcher (`py`) enabled. PostgreSQL and Redis are not needed for a basic
local run; the development settings use SQLite.

### macOS

1. Clone the repository (replace the placeholder with the repository URL):

	```sh
	git clone <repository-url> absolute-icecream
	cd absolute-icecream
	```

2. Create a virtual environment and install project requirements:

	```sh
	python3 -m venv .venv
	source .venv/bin/activate
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	```

3. Make a private local environment file:

	```sh
	cp .env.example .env
	```

	Edit `.env`. Set a unique, strong `SECRET_KEY` and `ADMIN_PASSWORD` for your
	local environment. Do not commit `.env` or use development secrets in
	production.

4. Apply database migrations and start Flask:

	```sh
	flask --app run.py db upgrade
	flask --app run.py --debug run
	```

5. Visit <http://127.0.0.1:5000>. Stop the server with Control-C. Run tests
	from the activated virtual environment with:

	```sh
	python -m pytest
	```

### Windows (PowerShell)

1. Clone the repository and enter its directory:

	```powershell
	git clone <repository-url> absolute-icecream
	Set-Location absolute-icecream
	```

2. Create a virtual environment, activate it, and install dependencies:

	```powershell
	py -3 -m venv .venv
	.\.venv\Scripts\Activate.ps1
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	```

	If PowerShell prevents activation, use `\.venv\Scripts\python.exe -m pip`
	for the pip commands and `\.venv\Scripts\python.exe -m flask` for Flask
	commands; activation is optional.

3. Create a private local environment file:

	```powershell
	Copy-Item .env.example .env
	```

	Edit `.env`. Set a unique, strong `SECRET_KEY` and `ADMIN_PASSWORD` for your
	local environment. Do not commit `.env` or use development secrets in
	production.

4. Apply database migrations and start Flask:

	```powershell
	python -m flask --app run.py db upgrade
	python -m flask --app run.py --debug run
	```

5. Visit <http://127.0.0.1:5000>. Stop the server with Control-C. Run tests
	from the activated virtual environment with:

	```powershell
	python -m pytest
	```

### Optional sample data

To populate local development data, launch the Flask shell after setting up
`.env`:

```sh
flask --app run.py shell
```

Then, at the Python prompt, run:

```python
from app.seed.seed_products import seed_products
seed_products()

from app.seed.admin import create_initial_admin
create_initial_admin()
```

On Windows, start the shell with `python -m flask --app run.py shell`. The
admin account is created using the `ADMIN_NAME`, `ADMIN_EMAIL`, and
`ADMIN_PASSWORD` values in `.env`. Only use non-production credentials locally.

## Keeping secrets out of Git

- `.env` and other local environment files, local databases, virtual
  environments, and common private key/credential files are excluded by
  `.gitignore`.
- `.env.example` is a placeholder template and remains trackable. Never put
  real passwords, API keys, tokens, or production database URLs in it.
- Before pushing changes, review `git status` and the staged diff for secrets.
  Ignore rules do not remove files already tracked or erase committed secrets
  from repository history. If a secret was exposed, revoke or rotate it.

## Optional Docker setup

Docker Compose can start the web app with PostgreSQL and Redis. Create `.env`
from `.env.example` first, replace local credentials, then run:

```sh
docker compose up --build
```

The app is available at <http://127.0.0.1:5000>. Stop the stack with
`docker compose down`; add `--volumes` only if you also intend to delete the
local PostgreSQL data volume.