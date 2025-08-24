import os, re, requests
from dotenv import load_dotenv, find_dotenv

def mask(s, show_start=6, show_end=4):
    if not s:
        return "<None>"
    if len(s) <= show_start + show_end:
        return s
    return f"{s[:show_start]}...{s[-show_end:]} (len={len(s)})"

# 1) Load .env explicitly from the current working directory (or nearest parent)
env_path = find_dotenv(usecwd=True)
print("Found .env at:", env_path if env_path else "<not found>")
load_dotenv(env_path, override=True)

# 2) Read the key exactly as Python sees it
raw = os.getenv("GROQ_API_KEY")
print("Raw env present? ", raw is not None)
print("Raw preview:     ", mask(raw))

# 3) Sanitize and validate (catch quotes/newlines/CR)
clean = (raw or "").strip().strip('"').strip("'").replace("\r", "").replace("\n", "")
print("Clean preview:   ", mask(clean))
print("Starts with gsk_:", clean.startswith("gsk_"))

if raw and raw != clean:
    print("Note: raw and clean differ -> you had quotes/newlines/CRLF. Cleaned in-memory.")

# 4) Extra safety: look for suspicious characters
if raw:
    bad = []
    if '"' in raw or "'" in raw: bad.append("quotes")
    if "\n" in raw: bad.append("\\n")
    if "\r" in raw: bad.append("\\r")
    if raw.endswith(" "): bad.append("trailing space")
    print("Suspicious chars:", bad or "none")

# 5) Quick fail-fast checks
if not clean:
    raise SystemExit("ERROR: GROQ_API_KEY is empty/missing.")
if not re.match(r"^gsk_[A-Za-z0-9]+$", clean):
    raise SystemExit("ERROR: Key format looks off (unexpected chars).")

# 6) Make a tiny live request to Groq
API_URL = "https://api.groq.com/openai/v1/chat/completions"
payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "Explain the importance of fast language models"}]}

try:
    resp = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {clean}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
        proxies={"http": None, "https": None},  # bypass env proxies
    )
    print("HTTP status:", resp.status_code)
    # Only print a short diagnostic so we don’t dump full responses
    text = resp.text
    print("Body preview:", text[:200] + ("..." if len(text) > 200 else ""))
except requests.RequestException as e:
    print("Network error:", e)
