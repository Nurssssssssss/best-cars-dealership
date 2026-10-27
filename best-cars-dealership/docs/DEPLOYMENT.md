# Deployment notes

This is a runnable development/demo project, not a production-ready SaaS deployment.

1. Build and test locally using README instructions.
2. For Docker: `docker build -t best-cars .` then `docker run --rm -p 8000:8000 -e DEBUG=1 -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 best-cars`.
3. For a hosted deployment, set `DEBUG=0`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, secure cookie settings, HTTPS, persistent database and storage. **SQLite in an ephemeral container will lose data on redeploy**; use managed PostgreSQL before production.
4. Deploy container to a service that supports Docker, or edit `deployment.yml` to set the image and hostname, create the secret, and apply it with `kubectl apply -f deployment.yml`.
5. Record the real deployment URL in `evidence/deploymentURL` and capture actual deployed screenshots.

Kubernetes manifest is a starting example; it does not include ingress, persistent storage, TLS, autoscaling, or managed database configuration. `docker-compose.yml` includes optional MongoDB/mongo-express to demonstrate containers; Django itself uses SQLite.
