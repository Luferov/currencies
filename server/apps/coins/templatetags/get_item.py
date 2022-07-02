from django.template.defaulttags import register


@register.filter
def get_item(dictionary: dict, key: str):
    return dictionary.get(key)
