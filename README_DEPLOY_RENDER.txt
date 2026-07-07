Render Settings:
Service Type: Web Service
Language: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app

Important:
- Do not deploy as Static Site.
- Do not upload .venv folder to GitHub.
- If app.py is inside a folder in GitHub, set Render Root Directory to that folder.
- .python-version is added to pin Python to 3.11.11 for stable pandas/openpyxl install.
