from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = Cart.objects.filter(user=None).count()

    return {'cart_count': count}