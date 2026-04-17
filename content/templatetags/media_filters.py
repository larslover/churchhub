from django import template
import re
import logging

register = template.Library()

logger = logging.getLogger(__name__)


@register.filter
def youtube_embed(value):
    """
    Converts YouTube URL to embed URL
    """
    if not value:
        return ""

    video_id = re.findall(r"(?:v=|youtu\.be/)([\w-]+)", value)

    if video_id:
        return f"https://www.youtube.com/embed/{video_id[0]}"

    return ""


@register.filter
def spotify_embed(value):
    """
    Converts Spotify track URL to embed URL
    """
    if not value:
        return ""

    match = re.search(r"spotify\.com/track/([A-Za-z0-9]+)", value)

    if match:
        return f"https://open.spotify.com/embed/track/{match.group(1)}"

    return value