# Best Cars Dealership Review Application

**Repository name:** `best-cars-dealership`  
**Project name:** Best Cars Dealership Review Application

A full-stack Django + React dealer directory with registration, login/logout, dealer search by state, dealer detail pages, reviews, and simple sentiment analysis. Includes seed data, a Dockerfile, Kubernetes manifests and GitHub Actions CI.

## Quick start (local)

Requirements: Python 3.11+, Node 20+.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server/manage.py migrate
python server/manage.py seed_demo
python server/manage.py createsuperuser
python server/manage.py runserver
```

In another terminal:

```bash
cd server/frontend
npm install
npm run dev
```

Open the React UI at http://localhost:5173 and Django API/admin at http://localhost:8000. React proxies `/api` and `/admin` to Django.

For a **single-server deployment**, build React with `npm run build` then run Django with `DJANGO_SERVE_REACT=1` and `DEBUG=0` after setting `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and a secure production database. See `docs/DEPLOYMENT.md`.

## API routes

- `GET /api/dealers/` list dealers; optional `?state=Kansas`
- `GET /api/dealers/<id>/` dealer details
- `GET /api/dealers/<id>/reviews/` dealer reviews
- `GET /api/carmakes/` car makes and models
- `GET /api/analyze/?text=Fantastic%20services` simple sentiment
- `POST /api/register/` username, first_name, last_name, email, password
- `POST /api/login/` username, password
- `POST /api/logout/` logout
- `POST /api/dealers/<id>/reviews/` rating, text, car_make, car_model, car_year, purchase_date (login required)

The project uses SQLite for easy local testing. The provided MongoDB and mongo-express services are **optional development tooling**, not the primary Django database. The sentiment classifier is a transparent keyword baseline, not a hosted IBM Watson model. For production, replace it with a trained or hosted service.

## Assignment submissions

`docs/SUBMISSION_CHECKLIST.md` maps tasks 1–28 to actual paths, cURL commands and required screenshots. `evidence/` contains **templates and scripts only**, not fabricated terminal outputs or screenshots. Run the app to generate authentic evidence before submission.
