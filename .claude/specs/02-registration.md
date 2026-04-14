---

# Spec: Registration

## Overview
Implement the user registration feature that allows visitors to create an account. This involves making the `/register` route handle POST requests, validating form data, hashing passwords with werkzeug, storing user data in SQLite, and establishing a session so the user is immediately logged in after registration.

## Depends on
- Step 1: Database Setup (users table already exists)

## Routes
- `POST /register` — Process registration form — public
  - Accepts: name, email, password
  - Validates: all fields present, email format, password length (min 8 chars)
  - On success: create user, set session, redirect to /profile
  - On failure: re-render register.html with error message

## Database changes
No database changes. The `users` table already exists with:
- `id`, `username`, `email`, `password_hash`, `created_at`

Note: The form uses `name` but the DB uses `username` — map accordingly.

## Templates
- **Modify:** `templates/register.html`
  - Ensure form `method="POST"` and `action="/register"` are correct
  - Display error messages from server (already has `{% if error %}` block)
  - Keep existing fields: name, email, password

## Files to change
- `app.py` — Add POST handler to `/register` route
- `templates/register.html` — Verify form setup (no changes likely needed)

## Files to create
None

## New dependencies
- `flask.session` — for session management
- `werkzeug.security.generate_password_hash` — already imported in db.py, import in app.py too

## Rules for implementation
- No SQLAlchemy or ORMs — use raw SQL with parameterised queries
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html` — already does
- Session secret key must be set (use `app.secret_key`)
- Flash messages or pass error as template variable
- After successful registration, set `session["user_id"]` and redirect to `/profile`
- Check for duplicate email or username and show appropriate error

## Definition of done
- [ ] Visiting `/register` shows the registration form
- [ ] Submitting empty fields shows error message
- [ ] Submitting duplicate email shows error message
- [ ] Submitting valid data creates a user in the database
- [ ] Password is stored hashed (not plaintext) in `password_hash` column
- [ ] After registration, user is redirected to `/profile`
- [ ] Session contains `user_id` matching the newly created user
- [ ] `/logout` route clears the session (placeholder removal)
