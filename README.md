# TUP Cavite · Office of Guidance Services

A Django homepage for TUP Cavite's Office of Guidance Services, with a Facebook post carousel and an **Access Portal** button leading to a SIBOL-inspired staff login page.

## Run locally (PowerShell)

```powershell
cd C:\Users\maeve\AndroidStudioProjects\OGSSERVICES\website\ogs_web
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/. **Access Portal** opens `/login/`. Local staff accounts and sessions use SQLite, which is excluded from Git.

## Staff sign-in

The login form uses Django's authentication, password hashing, CSRF protection, and sessions. Only active accounts with `is_staff=True` may sign in. `createsuperuser` creates an account with staff access; there are no shared default credentials. Successful sign-in opens a small authenticated account page at `/portal/`. Sign-out requires POST.

`.env.example` documents process environment variables; Django does not automatically load the file. The former `OGS_PORTAL_URL` setting is no longer used: the navigation always opens this site's login page.

## Checks

```powershell
python manage.py check
python manage.py test
```

## Deploy on Render

Create a **Web Service** from this repository with the **Python 3** runtime. Leave **Root Directory** empty: `manage.py` is at the repository root.

**Build command**

```sh
pip install -r requirements.txt && python build.py
```

**Start command**

```sh
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Set `DJANGO_DEBUG=false` and generate a random `DJANGO_SECRET_KEY` in Render's Environment settings. The Render service hostname is automatically allowed through `RENDER_EXTERNAL_HOSTNAME`. Set `DJANGO_ALLOWED_HOSTS` if you also use a custom domain.

For working staff accounts, add a persistent PostgreSQL `DATABASE_URL` to the Render web service. The build script automatically runs migrations when that variable exists. After deployment, run `python manage.py createsuperuser` in a shell connected to that database. If your Render plan does not provide a shell, run the command locally with the database's external URL in `DATABASE_URL`; keep that URL private. Staff sign-in stays disabled on Render until a persistent database is configured; the public homepage and login design remain available. Render's temporary local disk is never used for production staff accounts.

Alternatively, create a Render **Blueprint** from `render.yaml`; it configures both commands and generates the secret key. Supply `DATABASE_URL` separately to enable staff sign-in. WhiteNoise serves the collected assets in production.

## Content and assets

- The existing TUP seal was copied from `OGSSERVICES/branding/tup-seal.svg`.
- Icons are a bundled subset of Lucide Static 1.74.0, loaded in the initial HTML as an SVG sprite. They do not need an external CDN, JavaScript, or emoji fonts. The upstream license is included in `static/icons/LICENSE`.
- The hero displays a manually controlled carousel of the three selected Facebook posts, inspired by the embedded Facebook updates on [UniFAST](https://unifast.gov.ph/). Edit `home/posts.py` to change the list. Permanent post URLs were resolved from the supplied Facebook share links.
- Only the selected post is loaded initially; other embeds load on first selection. Previous/next buttons, pagination dots, and keyboard navigation (arrow keys, Home, End while using the controls) are supported. No autoplay interrupts reading. Each post includes a direct Facebook link, and all three links remain available without JavaScript.
- Facebook supplies the embedded content. Public-post availability, Facebook restrictions, browser privacy settings, and network access can affect rendering; the website cannot inspect or reliably detect errors inside a cross-origin Facebook frame.
- Design reference: [your SIBOL RSVP project](https://github.com/maeven-tapa/sibol_rvsp), including its cream/cardinal palette, serif headlines, and spacious introduction.
- Fonts: DM Sans, Manrope, and Playfair Display via Google Fonts, with local system fallbacks.
- Services, office hours, and campus location are based on [TUP Cavite's official OGS page](https://www.tupcavite.edu.ph/office/ogs). Inquiries link to official university channels; no invented email address or appointment form is used.
