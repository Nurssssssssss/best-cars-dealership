@echo off
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
python server\manage.py migrate
python server\manage.py seed_demo
start "Django" cmd /k "call .venv\Scripts\activate && python server\manage.py runserver"
cd server\frontend
call npm install
call npm run dev
