from users.choices import RoleChoice


def role_choices(request):
    """
    RoleChoice ni barcha template larga uzatish uchun context processor
    """
    return {
        'RoleChoice': RoleChoice
    }
