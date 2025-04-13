from django.http import HttpResponse
from django.template import loader
from .models import Auction
from django.shortcuts import render, redirect
from .forms import AuctionForm

def hello_view(request):
    name = request.GET.get('name', 'World')
    return render(request, 'auctions/hello.html', {'name': name})

def index(request):
    auctions = Auction.objects.all()
    template = loader.get_template("auctions/index.html")
    context = { "auction_list": auctions }
    return HttpResponse(template.render(context, request))

def detail(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    context = { "auction": auction }
    return render(request, "auctions/detail.html", context)

def create(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AuctionForm()
    return render(request, 'auctions/new.html', {'form': form})

def edit(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    
    if request.method == 'POST':
        form = AuctionForm(request.POST, instance=auction)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AuctionForm(instance=auction)
    
    return render(request, 'auctions/edit.html', {'form': form, 'auction': auction})

def delete(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    auction.delete()
    return redirect('index')
