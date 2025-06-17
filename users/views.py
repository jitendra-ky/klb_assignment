"""Views for the users app."""
from django.shortcuts import HttpResponse


# Create your views here.
def index(request: object) -> HttpResponse:
    """Display the users index page."""
    return HttpResponse(f"Hello, world. You're at the users index. {request}")
