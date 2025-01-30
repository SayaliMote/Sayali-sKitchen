from .models import Type

def menu_links(request):
    links = Type.objects.all()
    return {'links':links}
    