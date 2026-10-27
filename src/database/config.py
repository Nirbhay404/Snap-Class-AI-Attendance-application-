import base64
import json
import os
import streamlit as st
from supabase import create_client, Client

# Use Python 3.11+ built-in tomllib, fallback to toml if available
try:
    import tomllib
except ModuleNotFoundError:
    try:
        import toml as tomllib
    except ModuleNotFoundError:
        tomllib = None


def get_supabase_credentials():
    # 1. Try Streamlit secrets
    try:
        if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
            return st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
    except Exception:
        pass

    # 2. Try .streamlit/secrets.toml or streamlit/secrets.toml
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    candidate_paths = [
        os.path.join(root_dir, ".streamlit", "secrets.toml"),
        os.path.join(root_dir, "streamlit", "secrets.toml"),
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            try:
                if tomllib is not None:
                    # tomllib expects binary mode; toml handles binary or text
                    with open(p, "rb") as f:
                        data = tomllib.load(f)
                    if "SUPABASE_URL" in data and "SUPABASE_KEY" in data:
                        return data["SUPABASE_URL"], data["SUPABASE_KEY"]
            except Exception:
                pass

    # 3. Environment variables (no hardcoded defaults: credentials must never live in the repo)
    return os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")


url, key = get_supabase_credentials()

if not url or not key:
    raise RuntimeError(
        "Supabase credentials are missing. Set SUPABASE_URL and SUPABASE_KEY in "
        ".streamlit/secrets.toml (local) or in the app's Secrets settings (Streamlit Cloud). "
        "See SECURITY_SETUP.md."
    )

def _is_public_key(api_key: str) -> bool:
    if api_key.startswith("sb_publishable_"):
        return True
    if api_key.startswith("sb_secret_"):
        return False
    try:  # legacy JWT keys carry their role in the payload
        payload = api_key.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload)).get("role") == "anon"
    except Exception:
        return False


if _is_public_key(key):
    # Publishable/anon keys are visible to anyone, so with Row Level Security on they cannot reach the data.
    print(
        "WARNING: SUPABASE_KEY looks like a publishable/anon key. Use the secret/service-role key "
        "(see SECURITY_SETUP.md), otherwise the app breaks once Row Level Security is enabled."
    )
supabase: Client = create_client(url, key)