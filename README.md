# Absolute Icecream™

Premium D2C ice cream ecommerce platform.

## Brand

Real taste. No compromises.

## Technology

- Python
- Flask
- Jinja2
- HTML5
- CSS3
- JavaScript
- Tailwind CSS
- PostgreSQL
- SQLAlchemy
- Flask-Migrate
- Redis
- Celery
- Chart.js

## Development

### Prerequisites

- Git
- Python 3.10 or newer
- macOS Terminal or Windows PowerShell

The default development configuration uses SQLite, so PostgreSQL and Redis are
not required to run the web app locally. Do not use the development settings or
credentials for a public deployment.

### macOS

1. Clone the repository and enter the project directory:

	```sh
	git clone <repository-url> absolute-icecream
	cd absolute-icecream
	```

2. Create and activate a virtual environment, then install dependencies:

	```sh
	python3 -m venv .venv
	source .venv/bin/activate
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	```

3. Create your private local environment file and edit it in VS Code:

	```sh
	cp .env.example .env
	```

	Set a unique, strong `SECRET_KEY` and `ADMIN_PASSWORD` in `.env`. Keep the
	local SQLite `DATABASE_URL` unless you have configured another database.

4. Create/update the database schema and start the development server:

	```sh
	flask --app run.py db upgrade
	flask --app run.py --debug run
	```

5. Open <http://127.0.0.1:5000> in a browser. To run the test suite:

	```sh
	python -m pytest
	```

### Windows (PowerShell)

1. Clone the repository and enter the project directory:

	```powershell
	git clone <repository-url> absolute-icecream
	Set-Location absolute-icecream
	```

2. Create and activate a virtual environment, then install dependencies:

	```powershell
	py -3 -m venv .venv
	.\.venv\Scripts\Activate.ps1
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	```

	If PowerShell blocks environment activation, run the same Python commands
	with `.\.venv\Scripts\python.exe` instead of activating the environment.

3. Create your private local environment file and edit it in VS Code:

	```powershell
	Copy-Item .env.example .env
	```

	Set a unique, strong `SECRET_KEY` and `ADMIN_PASSWORD` in `.env`. Keep the
	local SQLite `DATABASE_URL` unless you have configured another database.

4. Create/update the database schema and start the development server:

	```powershell
	python -m flask --app run.py db upgrade
	python -m flask --app run.py --debug run
	```

5. Open <http://127.0.0.1:5000> in a browser. To run the test suite:

	```powershell
	python -m pytest
	```

### Optional local data

To populate the development database with the sample product catalogue, open
Flask's application shell after configuring `.env`:

```sh
flask --app run.py shell
```

Then run:

```python
from app.seed.seed_products import seed_products
seed_products()
```

Create the initial admin account using the `ADMIN_NAME`, `ADMIN_EMAIL`, and
`ADMIN_PASSWORD` values set in `.env`:

```python
from app.seed.admin import create_initial_admin
create_initial_admin()
```

On Windows, use `python -m flask --app run.py shell` to start the same shell.
These seed commands are optional; do not use sample credentials on a deployed
instance.

### Secrets and local files

- `.env` is for local secrets and is ignored by Git. Never commit it, paste
  credentials into source files, or add real tokens/passwords to this README.
- `.env.example` contains placeholders only and is safe to keep as a setup
  template. Replace its placeholder values in your private `.env` file.
- Local database files, virtual environments, and common private-key or
  credential files are also excluded by `.gitignore`.
- Before pushing, review `git status` and the staged diff. If a secret was ever
  committed or pushed, rotate/revoke it immediately; adding it to `.gitignore`
  does not remove it from Git history.