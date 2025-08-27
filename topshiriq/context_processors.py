from .services import XabarnomaService

def xabarlar_context(request):
    """Barcha sahifalarda bildirishnomalar ko'rsatish uchun context"""
    if request.user.is_authenticated:
        try:
            unread_count = XabarnomaService.get_unread_count(request.user)
            recent_xabarlar = XabarnomaService.get_recent_notifications(request.user, 5)
            
            return {
                'unread_xabarlar_count': unread_count,
                'recent_xabarlar': recent_xabarlar,
            }
        except:
            return {
                'unread_xabarlar_count': 0,
                'recent_xabarlar': [],
            }
    return {
        'unread_xabarlar_count': 0,
        'recent_xabarlar': [],
    }
