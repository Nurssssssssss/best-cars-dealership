# Coursera 28-task evidence checklist

**Never submit placeholders as genuine evidence.** This repository supplies implementation and capture scripts; actual evidence must come from running the app.

| Task | Evidence to submit | How to obtain |
|---|---|---|
| 1 | public README.md URL | Upload repository to GitHub and copy `/blob/main/README.md` URL |
| 2 | `django_server` terminal output | `python server/manage.py runserver 2>&1 | tee evidence/django_server` (Linux/macOS) |
| 3 | public `server/frontend/static/About.html` URL | Copy GitHub file URL; replace illustrative team/contact placeholders |
| 4 | public `server/frontend/static/Contact.html` URL | Copy GitHub file URL; replace placeholder contacts |
| 5 | `loginuser` cURL output | Create a valid account and run `scripts/capture_auth_evidence.sh` |
| 6 | `logoutuser` cURL output | Same script |
| 7 | public `server/frontend/src/components/Register/Register.jsx` URL | Copy GitHub file URL |
| 8 | `getdealerreviews` | `bash scripts/capture_api_evidence.sh` |
| 9 | `getalldealers` | Same script |
| 10 | `getdealerbyid` | Same script |
| 11 | `getdealersbyState` | Same script; Kansas seed records |
| 12 | `admin_login.png` | Screenshot actual `/admin/` authenticated as superuser |
| 13 | `admin_logout.png` | Screenshot actual `/admin/logout/` after logout |
| 14–15 | `getallcarmakes` | API evidence script |
| 16 | `analyzereview` | API evidence script, text=Fantastic services |
| 17 | `get_dealers.png` | Screenshot home `/` before login |
| 18 | `get_dealers_loggedin.png` | Screenshot home after login with username and address bar |
| 19 | `dealersbystate.png` | Screenshot `/?state=Kansas` with address bar |
| 20 | `dealer_id_reviews.png` | Screenshot `/dealer/1` with reviews and address bar |
| 21 | `dealership_review_submission.png` | Screenshot `/dealer/1/review` with completed fields before submission |
| 22 | `added_review.png` | Screenshot `/dealer/1` after posting review |
| 23 | `CI/CD` | Copy actual successful GitHub Actions run logs, do not fabricate |
| 24 | `deploymentURL` | Deploy app and record its real URL |
| 25 | `deployed_landingpage.png` | Screenshot deployed home page |
| 26 | `deployed_loggedin.png` | Screenshot deployed logged-in home page with username |
| 27 | `deployed_dealer_detail.png` | Screenshot deployed `/dealer/1` |
| 28 | `deployed_add_review.png` | Screenshot deployed posted review |

**Preparation:** run migrations, `seed_demo`, `createsuperuser`, Django server and React dev server. Create a regular user with the registration page. Post at least one review to populate dealer reviews. Capture all screenshots with the browser address bar visible where required. CI and deployment require actual GitHub/hosting setup.

**Important difference from the IBM reference project:** the assignment may expect specific original IBM API paths, MongoDB integration, and IBM Watson sentiment endpoint. This implementation provides equivalent demo functionality using different API paths and a keyword baseline. Check the course rubric and adapt if exact IBM architecture is mandatory.
