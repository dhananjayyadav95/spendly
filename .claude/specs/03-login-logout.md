---

# Spec: Login and Logout

## Overview
Implement the complete login and logout functionality that allows registered users to authenticate and end their session. This involves making the `/login` route handle POST requests with proper credential validation, and refining the `/logout` route to provide a smooth logout experience. This completes the authentication flow alongside the existing registration feature.

## Depends on
- Step 1: Database Setup (users table exists)
- Step 2: Registration (users can create accounts)

## Routes
- `POST /login` — Process login form — public
  - Accepts: email, password
  - Validates: email exists in database, password matches hash
  - On success: set `session["user_id"]`, redirect to `/profile`
  - On failure: re-render login.html with error message

- `GET /logout` — End user session — logged-in
  - Clears session
  - Redirects to `/` (landing page)

## Database changes
No database changes. The `users` table already exists with:
- `id`, `username`, `email`, `password_hash`, `created_at`

## Templates
- **Modify:** `templates/login.html`
  - Ensure form `method="POST"` and `action="/login"` are correct
  - Display error messages from server (add `{% if error %}` block if missing)
  - Keep existing fields: email, password

- **Modify:** `templates/base.html`
  - Update navigation to show logged-in state:
    - If logged in: show "Profile" and "Logout" links
    - If not logged in: show "Login" and "Register" links
  - Use `{% if session.get('user_id') %}` for conditional rendering

## Files to change
- `app.py` — Add POST handler to `/login` route, refine `/logout` route
- `templates/login.html` — Add error display block if missing
- `templates/base.html` — Update navigation for auth state

## Files to create
None

## New dependencies
No new dependencies. Uses existing:
- `flask.session` — already in use
- `werkzeug.security.check_password_hash` — for password verification

## Rules for implementation
- No SQLAlchemy or ORMs — use raw SQL with parameterised queries
- Use `werkzeug.security.check_password_hash` to verify passwords
- Generic error messages for failed login (don't reveal if email exists or password is wrong — use "Invalid credentials")
- Use CSS variables — never hardcode hex values
- All templates extend `base.html` — already does
- Session secret key is already set in `app.secret_key`
- After successful login, set `session["user_id"]` and redirect to `/profile`
- Logout clears entire session with `session.clear()`

## Definition of done
- [ ] Visiting `/login` shows the login form with email and password fields
- [ ] Submitting empty fields shows error message
- [ ] Submitting non-existent email shows generic "Invalid credentials" error
- [ ] Submitting wrong password shows generic "Invalid credentials" error
- [ ] Submitting valid credentials sets `session["user_id"]` and redirects to `/profile`
- [ ] Password verification uses `check_password_hash` (not plaintext comparison)
- [ ] `/logout` clears the session and redirects to landing page
- [ ] Navigation bar shows "Login/Register" when not logged in
- [ ] Navigation bar shows "Profile/Logout" when logged in
- [ ] After logging out, accessing `/profile` shows "coming soon" (not an error)
