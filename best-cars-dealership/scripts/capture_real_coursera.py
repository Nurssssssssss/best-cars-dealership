"""Capture real cURL results from a running Django server in CI.

Results are taken directly from curl stdout. The CI database and demo
accounts are ephemeral; these files do not prove public deployment.
"""
import json
import os
import shlex
import subprocess
from pathlib import Path

BASE = os.environ.get("EVIDENCE_BASE", "http://127.0.0.1:8000")
OUT = Path("evidence")
OUT.mkdir(exist_ok=True)


def curl_file(name, args):
    command = ["curl", "-sS", "--fail-with-body"] + args
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    try:
        formatted = json.dumps(json.loads(result.stdout), indent=2)
    except json.JSONDecodeError:
        formatted = result.stdout
    (OUT / name).write_text(
        "$ " + shlex.join(command) + "\n\n" + formatted + "\n",
        encoding="utf-8",
    )


for filename, endpoint in [
    ("getalldealers", "/fetchDealers"),
    ("getdealerbyid", "/fetchDealer/1"),
    ("getdealersbyState", "/fetchDealers/Kansas"),
    ("getdealerreviews", "/fetchReviews/dealer/1"),
    ("getallcarmakes", "/djangoapp/get_cars"),
    ("analyzereview", "/analyze/Fantastic%20services"),
]:
    curl_file(filename, ["-X", "GET", BASE + endpoint])

cookies = OUT / "temporary-cookiejar"
subprocess.run(
    ["curl", "-sS", "-c", str(cookies), BASE + "/api/csrf/"],
    capture_output=True, text=True, check=True,
)
tokens = [
    line.split()[-1]
    for line in cookies.read_text().splitlines()
    if "csrftoken" in line and not line.startswith("#")
]
if not tokens:
    raise RuntimeError("No CSRF cookie was issued by the server")

curl_file("loginuser", [
    "-X", "POST", "-b", str(cookies), "-c", str(cookies),
    "-H", "Content-Type: application/json",
    "-H", "X-CSRFToken: " + tokens[-1],
    "-d", json.dumps({"userName": "course_demo", "password": "DemoOnlyPass123!"}),
    BASE + "/djangoapp/login",
])
curl_file("logoutuser", [
    "-X", "GET", "-b", str(cookies), BASE + "/djangoapp/logout",
])
cookies.unlink(missing_ok=True)
(OUT / "README_EVIDENCE.md").write_text(
    "# Authentic CI evidence\n\n"
    "Commands and responses were captured from a temporary Django server "
    "inside GitHub Actions. Demo credentials are valid only in that CI run. "
    "Screenshots of the UI are from the temporary Vite/Django servers. "
    "Neither localhost URLs nor these files establish a public deployment.\n",
    encoding="utf-8",
)
print("Saved genuine cURL evidence from running CI server")
