from django.shortcuts import render, redirect
from main.models import Item, User
from django.views.decorators.cache import never_cache
from bson import ObjectId
from items.forms import *


# Create your views here.
@never_cache
def item_id(request, id: str):
    item = Item.find_one({"_id": ObjectId(id)})
    if not item:
        return render(request, "main/error.html")
    item_list = [it for it in Item.all() if it.id != item.id]
    params = {"item": item, "items": item_list[:4]}
    # if request.method == 'POST':

    if 'user' in request.session:
        params['form'] = CreateAuction()
    return render(request, "items/item.html", params)


def auction(request, id: str):
    return render(request, "items/auction.html", {"item": Item.find_one({"_id": ObjectId(id)}), "items": Item.all()[:4]})


def items(request):
    return render(request, 'items/items.html', {"items": Item.all()})


def add(request):
    if 'user' not in request.session:
        return redirect('Items')
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = Item.create(form.cleaned_data['name'], form.cleaned_data['description'],
                               owner=User.find_one({'name': request.session['user']['name']}).id)
            try:
                item.image = form.cleaned_data['image']
                item.save()
            except TypeError:
                item.save()

            return redirect('Item', id=item.id)
        else:
            print(form.errors)
    else:
        form = ItemForm()
    return render(request, "items/add_item.html", {"item": form})

