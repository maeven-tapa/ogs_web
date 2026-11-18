"""Selected public posts, in the order supplied for the homepage carousel."""
from urllib.parse import urlencode

FACEBOOK_POSTS = [
    {
        "title": "Welcoming first-year students and transferees",
        "url": "https://www.facebook.com/61568603414860/posts/122179663832620113/",
        "share_url": "https://www.facebook.com/share/p/1EXvjFjDnS/",
    },
    {
        "title": "Mental health awareness and suicide prevention seminar",
        "url": "https://www.facebook.com/61568603414860/posts/122187546764620113/",
        "share_url": "https://www.facebook.com/share/p/1AFur8P53x/",
    },
    {
        "title": "First-year students and transferees orientation at TUP Cavite",
        "url": "https://www.facebook.com/TeknArtisan/posts/1012338567563818/",
        "share_url": "https://www.facebook.com/share/p/1EBuj33uRF/",
    },
]

for post in FACEBOOK_POSTS:
    post["embed_url"] = "https://www.facebook.com/plugins/post.php?" + urlencode(
        {"href": post["url"], "show_text": "true", "width": 500}
    )
