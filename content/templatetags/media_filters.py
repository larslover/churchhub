from django import template
import re
import logging

register = template.Library()

# Configure logger for this module
logger = logging.getLogger(__name__)

@register.filter
def youtube_embed(value):
    """
    Converts a regular YouTube URL to an embeddable URL.
    Example: https://www.youtube.com/watch?v=aqz-KE-bpKQ
             -> https://www.youtube.com/embed/aqz-KE-bpKQ
    """
    if not value:
        logger.warning("youtube_embed called with empty value")
        return ""
    
    # Regex to capture the video ID
    video_id = re.findall(r"(?:v=|youtu\.be/)([\w-]+)", value)
    if video_id:
        embed_url = f"https://www.youtube.com/embed/{video_id[0]}"
        logger.info(f"youtube_embed: original='{value}' embed='{embed_url}'")
        return embed_url

    logger.warning(f"youtube_embed: could not parse URL '{value}'")
    return ""