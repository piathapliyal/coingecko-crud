This project is a Full Stack Developer demo task that showcases practical backend development skills using Django REST Framework and PostgreSQL.
It includes complete CRUD API endpoints, a third-party API integration (CoinGecko), and a simple reporting feature based on stored data.

Features

CRUD API-Create, Read, Update, and Delete items using REST APIs.
PostgreSQL Integration-All data is stored and managed in PostgreSQL.
Admin Panel-Django Admin enabled to manage records easily.
Third-Party API-Fetches live Bitcoin price data from CoinGecko.
Reporting Endpoint-Summarizes stored records for simple data insights.



Local Setup
1) Clone the Repository
git clone <your-github-repo-url>
cd coingecko-crud

2) Create Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate

3) Install Dependencies
pip install -r requirements.txt

4) Configure Database

Create a PostgreSQL DB:

CREATE DATABASE coingecko_db;


Update DATABASES in proj/settings.py if needed.

5) Apply Migrations
python manage.py migrate

6) Create Superuser
python manage.py createsuperuser

7) Run Server
python manage.py runserver


Visit: http://127.0.0.1:8000/admin