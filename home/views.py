from urllib.parse import urlsplit

from django.conf import settings
from django.shortcuts import render

from .posts import FACEBOOK_POSTS


def index(request):
    portal_url = settings.OGS_PORTAL_URL
    # Only use a full HTTP(S) URL; an unset destination opens an honest notice.
    parsed = urlsplit(portal_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        portal_url = ""
    return render(request, "home/index.html", {
        "portal_url": portal_url,
        "facebook_posts": FACEBOOK_POSTS,
    })
