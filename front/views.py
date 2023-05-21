from django.http import HttpResponse
from django.shortcuts import render, redirect

from front.forms import *

# Create your views here.

def main(request):
    if request.session.get("token", False):
        return redirect('/home')

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    if not request.session.get("token", False):
        return redirect('/')
    return render(request, 'home.html')

def login_post(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session["token"] = "sadssaadsa"
            return redirect('/home')
        else:
            return redirect('/')
    else:
        return redirect('/')
    
def logout(request):
    del request.session["token"]
    return redirect('/')

#################################
##  FORM PAGES
#################################

## ITEMS FORM PAGES
def search_item(request):
    if not request.session.get("token", False):
        return redirect('/')
    form = SearchItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Search Item', 'action': 'search_item_post'})
def get_all_items(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("get_all_items")
def update_item(request):
    if not request.session.get("token", False):
        return redirect('/')
    form = UpdateItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Update Item', 'action': 'update_item_post'})
def delete_item(request):
    if not request.session.get("token", False):
        return redirect('/')
    form = RemoveItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Delete Item', 'action': 'delete_item_post'})

## CAMPAIGN FORM PAGES
def create_campaign(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("create_campaign")
def add_request(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("add_request")
def get_request(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("get_request")
def update_request(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("update_request")
def remove_request(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("remove_request")
def query(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("query")
def watch(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("watch")
def unwatch(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("unwatch")

## REQUEST FORM PAGES
def mark_available(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("mark_available")
def pick(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("pick")
def arrived(request):
    if not request.session.get("token", False):
        return redirect('/')
    return HttpResponse("arrived")


#################################
##  POST PAGES
#################################

## ITEMS POST PAGES
def search_item_post(request):
    return redirect('/home')
def get_all_items_post(request):
    return redirect('/home')
def update_item_post(request):
    return redirect('/home')
def delete_item_post(request):
    return redirect('/home')

## CAMPAIGN POST PAGES
def create_campaign_post(request):
    return redirect('/home')
def add_request_post(request):
    return redirect('/home')
def get_request_post(request):
    return redirect('/home')
def update_request_post(request):
    return redirect('/home')
def remove_request_post(request):
    return redirect('/home')
def query_post(request):
    return redirect('/home')
def watch_post(request):
    return redirect('/home')
def unwatch_post(request):
    return redirect('/home')

## REQUEST POST PAGES
def mark_available_post(request):
    return redirect('/home')
def pick_post(request):
    return redirect('/home')
def arrived_post(request):
    return redirect('/home')