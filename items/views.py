from django.shortcuts import render
from django.http import HttpResponse
from main.models import Item, User
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def item_id(request, id: str):
    # Item.create('Mona Lisa', 'Manner of Leonardo da Vinci, circa 1900\n\nMona Lisa\n\noil on canvas, '
    #                          'unlined\nunframed: 79.1 x 54.6 cm.; 31⅛ x 21½ in.\n'
    #                          'framed: 96.4 x 71.9 cm.; 38 x 28¼ in',
    #             owner=User.find_one({'name': 'Denys'}))
    # return HttpResponse("<h1>item: "+id+"<h1>")
    return render(request, "main/item.html", {"item": Item.find_one({"_id": id}), "items": Item.all()[:4]})


def auction(request, id: str):
    return HttpResponse("<h1>auction of item: "+id+"<h1>")


def items(request):
    return render(request, 'main/items.html', {"items": Item.all()})
