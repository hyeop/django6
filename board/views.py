from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.
def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)
    
def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)


def index(request):
    kw = request.GET.get("kw", "")
    cate = request.GET.get("cate", "")
    pg = request.GET.get("page", 1)


    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            pass # 20일
            b = Board.objects.none()
    else:
        b = Board.objects.all()

    pag = Paginator(b, 3)
    obj = pag.get_page(pg)
    
    context = {
        "bset" : obj,
        "kw" : kw,
        "cate" : cate
    }
    return render(request, "board/index.html", context)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(b=b, replyer=request.user, 
    comment=c, pubdate=timezone.now()).save()
    return redirect("board:detail", bpk)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
        return redirect("board:detail", bpk)
    else:
        pass # 20 일차 (경고!!)
        return redirect("board:index")
    

def update(request, bpk):
    b = Board.objects.get(id=bpk)

    if b.writer != request.user:
        pass # 경고!!
        return redirect("board:index")

    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject, b.content = s, c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b" : b
    }
    return render(request, "board/update.html",context)


def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, writer=request.user, 
        content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else: # 무조건 불법적인 접근
        pass # 20 일 경고메세지
    return redirect("board:index")


def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rset" : r
    }
    return render(request, "board/detail.html", context)


