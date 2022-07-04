from django.shortcuts import render, redirect
from .models import Book

# Create your views here.
def create(request):
    if request.method == "POST":
        im = request.POST.get("impo")
        sn = request.POST.get("sname")  # [BOARD] :: C언어 
        su = request.POST.get("surl")   # /detail/1
        sc = request.POST.get("scon")
        Book(site_name=sn, site_url=su, site_con=sc, 
             impo=bool(im), maker=request.user).save()
        return redirect("book:index")

    return render(request, "book/create.html")

def index(request):
    b = request.user.book_set.all()
    context = {
        "bset" : b
    }
    return render(request, "book/index.html", context)