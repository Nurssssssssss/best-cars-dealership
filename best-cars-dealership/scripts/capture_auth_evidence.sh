#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE:-http://127.0.0.1:8000}"
USER_NAME="${USER_NAME:?Set USER_NAME to a valid existing account}"
PASSWORD="${PASSWORD:?Set PASSWORD to its password}"
mkdir -p evidence
COOKIE_FILE=$(mktemp); trap 'rm -f "$COOKIE_FILE"' EXIT
curl -s -c "$COOKIE_FILE" "$BASE/api/csrf/" >/dev/null
CSRF=$(awk '$6=="csrftoken"{print $7}' "$COOKIE_FILE")
LOGIN_PAYLOAD=$(python -c 'import json,os;print(json.dumps({"username":os.environ["USER_NAME"],"password":os.environ["PASSWORD"]}))')
{ echo "curl -i -b <cookiefile> -c <cookiefile> -H 'X-CSRFToken: <token>' -H 'Content-Type: application/json' -d '<credentials redacted>' '$BASE/api/login/'"; curl -i -s -b "$COOKIE_FILE" -c "$COOKIE_FILE" -H "X-CSRFToken: $CSRF" -H 'Content-Type: application/json' -d "$LOGIN_PAYLOAD" "$BASE/api/login/"; } > evidence/loginuser
{ echo "curl -i -b <cookiefile> -H 'X-CSRFToken: <token>' -H 'Content-Type: application/json' -d '{}' '$BASE/api/logout/'"; curl -i -s -b "$COOKIE_FILE" -H "X-CSRFToken: $CSRF" -H 'Content-Type: application/json' -d '{}' "$BASE/api/logout/"; } > evidence/logoutuser
printf 'Auth evidence saved; credentials were redacted from evidence files.\n'
