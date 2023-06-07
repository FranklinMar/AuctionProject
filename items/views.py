from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Item, User
from django.views.decorators.cache import never_cache
from bson import ObjectId
from items.forms import *
from django.http import HttpResponseRedirect


# Create your views here.
@never_cache
def item_id(request, id: str):
    item = Item.find_one({"_id": ObjectId(id)})
    item_list = [it for it in Item.all() if it.id != item.id]
    params = {"item": item, "items": item_list[:4]}
    if 'name' in request.session:
        params['form'] = CreateAuction()
    return render(request, "items/item.html", params)


def auction(request, id: str):
    return render(request, "items/auction.html", {"item": Item.find_one({"_id": ObjectId(id)}), "items": Item.all()[:4]})


def items(request):
    return render(request, 'items/items.html', {"items": Item.all()})


def add(request):
    if 'name' in request.session:
        if request.method == 'POST':
            print("SECTOR 1")
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                print("SECTOR 2")
                item = Item.create(form.cleaned_data['name'], form.cleaned_data['description'],
                                   owner=User.find_one({'name': request.session['name']}).id,
                                   image=form.cleaned_data['image'])

                print("SECTOR 3")
                return redirect('Item', id=item.id)
        return render(request, "items/add_item.html", {"item": ItemForm()})
    return redirect('Items')

