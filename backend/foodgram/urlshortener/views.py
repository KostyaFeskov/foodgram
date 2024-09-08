from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

from django.views.decorators.http import require_GET

from .models import LinkShortener


@require_GET
def url_load(request, url_hash: str) -> HttpResponse:

    url_original = get_object_or_404(
        LinkShortener, url_hash=url_hash
    ).url_original
    return redirect(url_original)
