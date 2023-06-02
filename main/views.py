from django.shortcuts import render
from .models import *
from django.views.decorators.cache import never_cache
from .forms import UploadFileForm


# Create your views here.
@never_cache
def home(request):
    # if request:
    # print(User.objects.first().items)
    # users = DB["User"]
    # if request.method == "POST":
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         file = request.FILES.get('file')
    #         Image.open(file).verify()
    #         print(type(file).__name__)
    #         print(file.content_type)
    #         user = User("Den", "nopointinliving", "denisbereznuuk@gmail.com", 0, image=file)
    # else:
    #     form = UploadFileForm()
    # user = users.find_one()
    # print(type(user["_id"]))
    # return HttpResponse(f"<h1>Hello world<h1>{user['name']}")
    return render(request, 'main/home.html', {"items": Item.all()})  # {"form": form}
