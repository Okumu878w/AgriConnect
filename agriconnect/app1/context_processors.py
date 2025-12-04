from .models import SavedItem

def saved_items_processor(request):
    if request.user.is_authenticated:
        saved_items = SavedItem.objects.filter(user=request.user).select_related('product')
        return {'saved_items': saved_items}
    return {'saved_items': []}