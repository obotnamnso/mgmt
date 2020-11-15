from django.shortcuts import render
from .models import Stock

# Create your views here.
def home(request):
    title = "Home"
    context = {
        "title": title
    }
    return render(request, "stockmgmt/home.html", context)

def list_item(request):
    title = "List Item"
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset
    }
    return render(request, "stockmgmt/list_item.html", context)