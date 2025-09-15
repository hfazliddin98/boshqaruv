from django import template
from users.choices import RoleChoice

register = template.Library()

@register.simple_tag
def get_all_roles():
    """Barcha rollarni qaytaradi"""
    return RoleChoice.choices
