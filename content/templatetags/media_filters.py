from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed(url):
    """
    Convert standard YouTube URL to embed format.
    Handles:
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID
    - Already embed URLs
    """
    if not url:
        return ""
    
    # Already an embed URL
    if "youtube.com/embed/" in url:
        return url

    # Short URL format
    if "youtu.be" in url:
        video_id = url.split("/")[-1].split("?")[0]  # Remove any params like ?t=123
        return f"https://www.youtube.com/embed/{video_id}"

    # Standard URL format
    if "youtube.com/watch" in url:
        query = urlparse(url).query
        video_id_list = parse_qs(query).get("v")
        if video_id_list:
            return f"https://www.youtube.com/embed/{video_id_list[0]}"

    return url