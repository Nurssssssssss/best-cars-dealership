# Best Cars Dealership Review Application

**Repository name:** `best-cars-dealership`  
**Project name:** Best Cars Dealership Review Application

This is a Django + React full-stack capstone project. Visitors can browse dealerships and reviews. Registered users can log in, select dealerships, and post reviews. An admin interface provides access to dealership and car model records.

## Project files

The complete application, installation steps, and API documentation are in [best-cars-dealership/README.md](best-cars-dealership/README.md).

- [Django backend](best-cars-dealership/server/)
- [React frontend](best-cars-dealership/server/frontend/)
- [Registration component](best-cars-dealership/server/frontend/src/components/Register/Register.jsx)
- [About Us](best-cars-dealership/server/frontend/static/About.html)
- [Contact Us](best-cars-dealership/server/frontend/static/Contact.html)
- [GitHub Actions](.github/workflows/)
- [Render deployment blueprint](render.yaml)

## Testing and submission evidence

GitHub Actions builds the code, exercises the API and creates actual browser screenshots of the temporary Django/React test environment. Open the **Actions** tab and download the `coursera-real-ci-evidence` artifact from a successful `Coursera genuine evidence` run.

The demo dealer data is synthetic. Screenshots from the temporary CI environment are not screenshots of a publicly deployed application. A Render web service must be deployed separately to obtain a real public URL.

## Deploy the working application

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Nurssssssssss/best-cars-dealership)

Click the button, review the service and approve deployment in your Render account. The included `render.yaml` requests a free Docker web service. On success, Render will show the actual `*.onrender.com` deployment URL. This action is separate from GitHub Actions and cannot be simulated by CI screenshots.

After the public Render URL appears, capture Task 25–28 screenshots automatically:

1. Open [GitHub Actions — Capture real public deployment screenshots](https://github.com/Nurssssssssss/best-cars-dealership/actions/workflows/capture-deployed.yml).
2. Choose **Run workflow** and enter your real `https://...onrender.com` URL.
3. Download the generated `coursera-real-deployment-evidence` ZIP artifact from the completed run. It contains `deployed_landingpage.png`, `deployed_loggedin.png`, `deployed_dealer_detail.png` and `deployed_add_review.png`. The workflow registers a new demonstration account and posts a sample review to the deployed test application.

Only use screenshots generated from a genuinely published URL. GitHub CI localhost evidence is for Tasks 1–23, not proof of public deployment.
