from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import csv
from .models import *
from .forms import *

# Create your views here.
def home(request):
    title = "Home"
    context = {
        "title": title
    }
    return render(request, "stockmgmt/home.html", context)

def list_items(request):
    header = "LIST OF PRODUCTS"
    form = StockSearchForm(request.POST or None)  #inputing the form search.
    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value()
                                        )
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY','ITEM NAME','QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

        context = {
                "form": form,
                "header": header,
                "queryset": queryset,
            }
    return render(request, "stockmgmt/list_items.html", context)
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item added Succssfully')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item"
    }
    return render(request, "stockmgmt/add_items.html", context)
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == "POST":
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succssfully Updated')
            return redirect('/list_items')
    context = {
        "form": form
    }
    return render(request, 'stockmgmt/add_items.html', context)

def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request,'Succssfully Updated')
        return redirect('/list_items')
    return render(request, 'stockmgmt/delete_items.html')

def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stockmgmt/stock_detail.html", context)
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        messages.success(request, "Issued SUCCESSFULLY." + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
        instance.save()
        return redirect('/stock_detail/'+str(instance.id))
    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "stockmgmt/add_items.html", context)


def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY." + str(instance.quantity) + " " + str(instance.item_name)+"s now in store")
        return redirect('/stock_detail/'+str(instance.id))
    context = {
        "title": 'Receive ' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
        }
    return render(request, "stockmgmt/add_items.html", context)
