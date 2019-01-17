from mainapp.models import get_menu


def menu(request):
    return {'menu': get_menu()}
