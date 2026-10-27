#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE:-http://127.0.0.1:8000}"
mkdir -p evidence
# The next commands capture real outputs from a running server; they do NOT invent responses.
{ echo "curl -i '$BASE/api/dealers/'"; curl -i "$BASE/api/dealers/"; } > evidence/getalldealers
{ echo "curl -i '$BASE/api/dealers/1/'"; curl -i "$BASE/api/dealers/1/"; } > evidence/getdealerbyid
{ echo "curl -i '$BASE/api/dealers/?state=Kansas'"; curl -i "$BASE/api/dealers/?state=Kansas"; } > evidence/getdealersbyState
{ echo "curl -i '$BASE/api/dealers/1/reviews/'"; curl -i "$BASE/api/dealers/1/reviews/"; } > evidence/getdealerreviews
{ echo "curl -i '$BASE/api/carmakes/'"; curl -i "$BASE/api/carmakes/"; } > evidence/getallcarmakes
{ echo "curl -i '$BASE/api/analyze/?text=Fantastic%20services'"; curl -i "$BASE/api/analyze/?text=Fantastic%20services"; } > evidence/analyzereview
printf 'API evidence saved. For login/logout, use scripts/capture_auth_evidence.sh.\n'
