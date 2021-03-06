from mainapp.models import get_menu
from cartapp.models import Cart
from wishapp.models import Wish


def menu(request):
    context = {'menu': get_menu()}
    if request.user.is_authenticated:
        context.update({#'cart': Cart.objects.filter(user=request.user).select_related(),
                        'cart': request.user.cart.select_related(),
                        #'wish': Wish.objects.filter(user=request.user),
                        'wish': request.user.wish.select_related(),
                        })
    return context
