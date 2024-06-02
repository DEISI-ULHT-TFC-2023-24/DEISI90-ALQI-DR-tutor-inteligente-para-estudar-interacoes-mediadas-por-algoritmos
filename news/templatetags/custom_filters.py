from datetime import datetime

from django import template
from django.templatetags.static import static as django_static

register = template.Library()

@register.filter
def get_options(snippet_options, snippet_id):
    return snippet_options.get(snippet_id, [])

@register.filter
def is_not_digit(value):
    return not value.isdigit()


@register.simple_tag
def category_image(category):
    file_path = f"images/{category}.png"
    return django_static(file_path)


@register.simple_tag
def source_image(source):
    formatted_category = source.source_name.lower().replace(" ", "_")
    formatted_category = formatted_category.replace("%20", "_")
    file_path = f"images/{formatted_category}.png"
    return django_static(file_path)


@register.filter
def date_parse(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


@register.filter
def page_range(value, page_window):
    """Generate a range of page numbers for pagination."""
    current_page = value.number
    total_pages = value.paginator.num_pages
    start = max(1, current_page - page_window)
    end = min(total_pages, current_page + page_window)

    return range(start, end + 1)


@register.filter(name='contains')
def contains(value, arg):
    if isinstance(value, str):
        return arg in value
    return False
