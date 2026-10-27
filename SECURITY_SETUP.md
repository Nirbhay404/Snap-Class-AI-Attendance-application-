# 🔒 Securing the SnapClass database

SnapClass talks to Supabase from the Streamlit server. Earlier versions used a **publishable (anon) key**
that was written into the repository, and the tables had no Row Level Security (RLS). Anyone who found the
key could read teacher password hashes and students' face and voice embeddings.

The code now reads its credentials only from secrets / environment variables. Follow these steps **in order**.

## 1. Get the secret key

In the Supabase dashboard open **Project Settings → API Keys** and copy the **secret key** (`sb_secret_…`).
On older projects this is the `service_role` key under *Legacy API keys*.

> The secret key bypasses RLS. Keep it in secrets only. Never commit it or paste it in the browser.
> Streamlit runs the database calls on the server, so the key is never sent to visitors.

## 2. Add it to your secrets

- **Local:** `.streamlit/secrets.toml` (already git-ignored)
- **Streamlit Cloud:** *Manage app → Settings → Secrets*

```toml
SUPABASE_URL = "https://<your-project-id>.supabase.co"
SUPABASE_KEY = "sb_secret_..."
```

## 3. Deploy and check the app still works

Reboot the app and log in as a teacher and as a student. The console prints a warning if `SUPABASE_KEY`
still looks like a public key.

## 4. Turn on Row Level Security

Open **SQL Editor** in Supabase, paste the contents of [`supabase/enable_rls.sql`](supabase/enable_rls.sql)
and run it. Every table in the result should show `rowsecurity = true`. Reload the app and confirm it still works.

## 5. Retire the exposed key

The old publishable key is permanently in the repository's git history, so treat it as public.
In **Project Settings → API Keys**, delete (or regenerate) the publishable key. If you use legacy keys,
rotate the JWT secret instead. The app no longer uses it.

## 6. Verify

Using the **old** key, a request should now return an empty list or an error, never your data:

```bash
curl -s "$SUPABASE_URL/rest/v1/teachers?select=username&limit=1" \
  -H "apikey: <old key>" -H "Authorization: Bearer <old key>"
```

## Good to know

- Face and voice embeddings are biometric data. Keep the secret key private and limit who can open the Supabase project.
- Passwords are stored as bcrypt hashes, but with open access those hashes could be copied and cracked offline.
  Consider asking teachers to choose new passwords after the key is retired.
