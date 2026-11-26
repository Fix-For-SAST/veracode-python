# homeController.py deals with the default website redirection.

from django.shortcuts import redirect
from .userController import login
import urllib

# redirects user to feed if they are already logged in, otherwise sends to login
def home(request):
    # Equivalent of HomeController.java
    if request.session.get('username'):
        # START BAD CODE
        try:
            # CWE-73 Fix: Define allowed URLs to prevent path traversal
            # TODO: Replace these placeholder values with actual allowed URLs for your application
            ALLOWED_URLS = [
                "http://localhost:8000/feed",
                "http://127.0.0.1:8000/feed",
                "http://yourapp.example.com:8000/feed"
            ]

            # Construct the requested URL from user input
            host_ip = request.META['HTTP_HOST'].split(':')[0]
            requested_url = 'http://' + host_ip + ':' + request.META['SERVER_PORT'] + '/feed'

            # Validate against allow-list and retrieve the matching static URL
            if requested_url not in ALLOWED_URLS:
                raise ValueError(f'Invalid URL requested: {requested_url}')
            else:
                url_index = ALLOWED_URLS.index(requested_url)
                safe_url = ALLOWED_URLS[url_index]  # Use the matching untainted URL

            print("da")
            redir = urllib.request.Request(safe_url)
            urllib.request.urlopen(redir, timeout=5)
        # END BAD CODE
        except: 
            # GOOD CODE:
            print("redir")
            return redirect('feed')
    
    return login(request)