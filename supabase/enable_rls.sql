-- Locks every SnapClass table so the public (anon/publishable) API key can no longer read or write it.
-- The app uses the secret / service-role key, which bypasses Row Level Security, so it keeps working.
--
-- RUN THIS ONLY AFTER the app is already using the secret key (see SECURITY_SETUP.md, step 3),
-- otherwise the app will see empty tables.

alter table public.teachers         enable row level security;
alter table public.students         enable row level security;
alter table public.subjects         enable row level security;
alter table public.subject_students enable row level security;
alter table public.attendance_logs  enable row level security;

-- No policies are created on purpose: with RLS on and no policy, anon and authenticated roles get no access.

-- Check: every row below should show rowsecurity = true
select tablename, rowsecurity
from pg_tables
where schemaname = 'public'
  and tablename in ('teachers', 'students', 'subjects', 'subject_students', 'attendance_logs');
