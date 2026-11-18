# TUP Cavite · Office of Guidance Services

A single-page Django website with TUP branding, a responsive navigation bar, service information, and a configurable **Access Portal** button. No accounts, booking system, or other application pages are included.

## Run locally (PowerShell)

```powershell
cd C:\Users\maeve\AndroidStudioProjects\OGSSERVICES\website\ogs_web
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/. The homepage does not need a database or migrations.

## Connect the portal

Set the destination before starting Django:

```powershell
$env:OGS_PORTAL_URL = 'https://your-actual-ogs-portal.example/'
python manage.py runserver
```

When unset, **Access Portal** opens a notice explaining that the portal is not yet connected and links to the official OGS page. It does not pretend to sign anyone in. `.env.example` documents environment variables; Django does not automatically load that file.

## Checks

```powershell
python manage.py check
python manage.py test
```

## Deploy on Render

Create a **Web Service** from this repository with the **Python 3** runtime. Leave **Root Directory** empty: `manage.py` is at the repository root.

**Build command**

```sh
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start command**

```sh
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Set `DJANGO_DEBUG=false` and generate a random `DJANGO_SECRET_KEY` in Render's Environment settings. The Render service hostname is automatically allowed through `RENDER_EXTERNAL_HOSTNAME`. Set `DJANGO_ALLOWED_HOSTS` if you also use a custom domain. Set `OGS_PORTAL_URL` when your portal destination is ready.

Alternatively, create a Render **Blueprint** from the included `render.yaml`; it configures both commands and generates the secret key. WhiteNoise serves the collected CSS, JavaScript, and images in production. This homepage does not require a database or a migration command.

## Content and assets

- The existing TUP seal was copied from `OGSSERVICES/branding/tup-seal.svg`.
- The hero displays a manually controlled carousel of the three selected Facebook posts, inspired by the embedded Facebook updates on [UniFAST](https://unifast.gov.ph/). Edit `home/posts.py` to change the list. Permanent post URLs were resolved from the supplied Facebook share links.
- Only the selected post is loaded initially; other embeds load on first selection. Previous/next buttons, pagination dots, and keyboard navigation (arrow keys, Home, End while using the controls) are supported. No autoplay interrupts reading. Each post includes a direct Facebook link, and all three links remain available without JavaScript.
- Facebook supplies the embedded content. Public-post availability, Facebook restrictions, browser privacy settings, and network access can affect rendering; the website cannot inspect or reliably detect errors inside a cross-origin Facebook frame.
- Design reference: [your SIBOL RSVP project](https://github.com/maeven-tapa/sibol_rvsp), including its cream/cardinal palette, serif headlines, and spacious introduction.
- Fonts: DM Sans, Manrope, and Playfair Display via Google Fonts, with local system fallbacks.
- Services, office hours, and campus location are based on [TUP Cavite's official OGS page](https://www.tupcavite.edu.ph/office/ogs). Inquiries link to official university channels; no invented email address or appointment form is used.
