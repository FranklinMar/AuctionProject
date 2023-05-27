from django.shortcuts import render
from .models import *
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def home(request):
    # if request:
    # print(User.objects.first().items)
    users = DB["User"]
    # user = User("Den", "denisbereznuuk@gmail.com", 0)
    user = users.find_one()
    print(type(user["_id"]))
    # return HttpResponse(f"<h1>Hello world<h1>{user['name']}")
    return render(request, 'main/home.html')
