# data_splitter/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Template filter para acceder a valores de diccionario por clave"""
    return dictionary.get(key)