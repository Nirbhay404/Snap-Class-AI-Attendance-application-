import os
import streamlit as st
import toml
from supabase import create_client, Client

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
                data = toml.load(p)
                if "SUPABASE_URL" in data and "SUPABASE_KEY" in data:
                    return data["SUPABASE_URL"], data["SUPABASE_KEY"]
            except Exception:
                pass

    # 3. Environment variables or defaults
    url = os.getenv("SUPABASE_URL", "https://pgwaxqzfmquvrrqdnwyx.supabase.co")
    key = os.getenv("SUPABASE_KEY", "sb_publishable_N1dOVh0qNIk632AN1AEkmA_-wQTeOYh")
    return url, key

url, key = get_supabase_credentials()
supabase: Client = create_client(url, key)