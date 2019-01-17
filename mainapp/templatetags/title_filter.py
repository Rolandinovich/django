from django import template

register = template.Library()

# фильтрация по строке поиска
@register.filter(name='title_filter')
def title_filter(source, search_str):
    return (itm for itm in source if itm.title.find(search_str))
