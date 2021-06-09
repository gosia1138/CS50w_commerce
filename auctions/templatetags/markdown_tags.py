from django import template
from markdown2 import markdown
import re

register = template.Library()

@register.filter
def markdown_on(value):
    return markdown(value)

@register.filter
def markdown_off(value):
    # Remove all html tags from text
    cleaner = re.compile('<.*?>')
    return re.sub(cleaner, '', markdown(value))
