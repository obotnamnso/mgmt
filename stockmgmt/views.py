from django.shortcuts import render
from .models import Stock
from .forms import StockCreateForm

# Create your views here.
def home(request):
    title = "Home"
    context = {
        "title": title
    }
    return render(request, "stockmgmt/home.html", context)

def list_items(request):
    title = "List Item"
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset
    }
    return render(request, "stockmgmt/list_items.html", context)
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        "form": form,
        "title": "Add Item"
    }
    return render(request, "stockmgmt/add_items.html", context)