from django.http import HttpResponse
from django.shortcuts import render, redirect

from front.forms import *
from front.socket import DjangoSocket, socket_service, get_watches

import threading

test_socket = DjangoSocket()
test_socket.start()

# Create your views here.

def main(request):
    if request.session.get('token', False):
        campaign = request.session.get("campaign", False)
        username = request.session.get("username", "")
        watches = get_watches(request.session.get('token'))
        return redirect('/home', {'campaign': campaign, 'username': username, 'watches': watches})

    form = LoginForm()
    return redirect('/login', {'form': form})

def home(request):
    if not request.session.get('token', False):
        campaign = request.session.get("campaign", False)
        return redirect('/login')
    campaign = request.session.get("campaign", False)
    username = request.session.get("username", "")
    watches = get_watches(request.session.get('token'))
    if watches == []:
        watches = ""
    return render(request, 'home.html', {'campaign': campaign, 'username': username, 'watches': watches})

def login(request):
    if request.session.get('token', False):
        return redirect('/home')
    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'title': 'Login', 'action': 'login_post'})


def logout(request):
    received = socket_service(f"{request.session.get('token')} logout", test_socket)
    if "Logout successful" in received:
        request.session.flush()
    return redirect('/')

#################################
#  LOGIN POST 
#################################

def login_post(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        login_txt = "login " + form.cleaned_data["username"] + " " + form.cleaned_data["password"]
        print(login_txt)
        received = socket_service(login_txt, test_socket)
        if "Login successful" in received:
            request.session['token'] = received.split(" ")[3]
            request.session['username'] = form.cleaned_data["username"]
            return redirect('/home', {'campaign': False, 'username': form.cleaned_data["username"]})
        else:
            return render(request, 'form_page.html', {'form': form, 'title': 'Login', 'action': 'login_post'})
    else:
        return render(request, 'form_page.html', {'form': form, 'title': 'Login', 'action': 'login_post'})

#################################
#  FORM PAGES
#################################


# CAMPAIGN FORM PAGES
def create_campaign(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = CreateCampaignForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Create Campaign', 'action': 'create_campaign_post'})


def list_campaigns(request):
    if not request.session.get('token', False):
        return redirect('/login')
    received = socket_service(f"{request.session.get('token')} list", test_socket)
    if "##EOF##" in received:
        received = received.replace("##EOF##", "")
    campaigns = received.split("\t")
    return render(request, 'result.html', {'result': campaigns})


def open_campaign(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = OpenCampaignForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Open Campaign', 'action': 'open_campaign_post'})


def close_campaign(request):
    create_txt = request.session.get('token') + " close"
    received = socket_service(create_txt, test_socket)
    del request.session["campaign"]
    return render(request, 'result.html', {'result': received})


# ITEMS FORM PAGES
def search_item(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = SearchItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Search Item', 'action': 'search_item_post'})


def update_item(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = UpdateItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Update Item', 'action': 'update_item_post'})


def delete_item(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = RemoveItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Delete Item', 'action': 'delete_item_post'})


# CAMPAIGN OPERATIONS FORM PAGES
def add_request(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = AddRequestForm()
    return render(request, 'form_page_itemreq.html', {'form': form, 'title': 'Add Request', 'action': 'add_request_post'})


def get_all_requests(request):
    if not request.session.get('token', False):
        return redirect('/login')
    received = socket_service(f"{request.session.get('token')} get_all_requests", test_socket)
    requests = received.split("\n")
    return render(request, 'result.html', {'result': requests, 'title': 'All Requests In Campaign'})


def get_request(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = GetRequestForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Get Request', 'action': 'get_request_post'})


def update_request(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = UpdateRequestForm()
    return render(request, 'form_page_itemreq.html', {'form': form, 'title': 'Update Request', 'action': 'update_request_post'})


def remove_request(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = RemoveRequestForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Remove Request', 'action': 'remove_request_post'})


def query_rect(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = QueryRectForm()
    return render(request, 'form_page_item.html', {'form': form, 'title': 'Query Rect', 'action': 'query_rect_post'})


def query_circle(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = QueryCircleForm()
    return render(request, 'form_page_item.html', {'form': form, 'title': 'Query Circle', 'action': 'query_circle_post'})


def watch_rect(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = WatchRectForm()
    return render(request, 'form_page_item.html', {'form': form, 'title': 'Watch Rect', 'action': 'watch_rect_post'})


def watch_circle(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = WatchCircleForm()
    return render(request, 'form_page_item.html', {'form': form, 'title': 'Watch Circle', 'action': 'watch_circle_post'})


def unwatch(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = UnwatchForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Unwatch', 'action': 'unwatch_post'})


# REQUEST FORM PAGES
def mark_available(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = MarkAvailableForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Mark Available', 'action': 'mark_available_post'})


def pick(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = PickForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Pick', 'action': 'pick_post'})


def arrived(request):
    if not request.session.get('token', False):
        return redirect('/login')
    form = ArrivedForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Arrived', 'action': 'arrived_post'})

#################################
#  POST PAGES
#################################

# ITEMS POST PAGES
def search_item_post(request):
    if request.method == 'POST':
        form = SearchItemForm(request.POST)
        if form.is_valid():
            search_txt = request.session.get('token') + " search_item " + form.cleaned_data['name']
            received = socket_service(search_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})

def update_item_post(request):
    if request.method == 'POST':
        form = UpdateItemForm(request.POST)
        if form.is_valid():
            update_txt = f"{request.session.get('token')} update_item {form.cleaned_data['target']} {form.cleaned_data['name']} {form.cleaned_data['synonyms']}"
            received = socket_service(update_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def delete_item_post(request):
    if request.method == 'POST':
        form = RemoveItemForm(request.POST)
        if form.is_valid():
            delete_txt = request.session.get('token') + " remove_item " + form.cleaned_data['name']
            received = socket_service(delete_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


# CAMPAIGN POST PAGES
def create_campaign_post(request):
    if request.method == 'POST':
        form = CreateCampaignForm(request.POST)
        if form.is_valid():
            create_txt = f"{request.session.get('token')} new {form.cleaned_data['name']} {form.cleaned_data['description']}"
            received = socket_service(create_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    else:
        return render(request, 'result.html', {'result': "Invalid request"})


def open_campaign_post(request):
    if request.method == 'POST':
        form = OpenCampaignForm(request.POST)
        if form.is_valid():
            open_txt = request.session.get('token') + " open " + form.cleaned_data['name']
            received = socket_service(open_txt, test_socket)
            if "Campaign opened" in received:
                request.session["campaign"] = form.cleaned_data['name']
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    else:
        return render(request, 'result.html', {'result': "Invalid request"})


def add_request_post(request):
    if request.method == 'POST':
        data = request.POST.dict()
        form = AddRequestForm(request.POST)
        if form.is_valid():
            item = " "
            for i in range(int(data['item_count'])):
                item += data[f"item{i+1}"] + " " + data[f"amount{i+1}"] + " "

            add_txt = f"{request.session.get('token')} add_request{item}{form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['urgency']} {form.cleaned_data['description']}"
            received = socket_service(add_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def get_request_post(request):
    if request.method == 'POST':
        form = GetRequestForm(request.POST)
        if form.is_valid():
            get_txt = request.session.get('token') + " get_request " + form.cleaned_data['request']
            received = socket_service(get_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def update_request_post(request):
    if request.method == 'POST':
        data = request.POST.dict()
        form = UpdateRequestForm(request.POST)
        if form.is_valid():
            item = " "
            for i in range(int(data['item_count'])):
                item += data[f"item{i+1}"] + " " + data[f"amount{i+1}"] + " "
            update_txt = f"{request.session.get('token')} update_request {form.cleaned_data['request']}{item}{form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['urgency']} {form.cleaned_data['description']}"
            received = socket_service(update_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def remove_request_post(request):
    if request.method == 'POST':
        form = RemoveRequestForm(request.POST)
        if form.is_valid():
            remove_txt = request.session.get('token') + " remove_request " + form.cleaned_data['request']
            received = socket_service(remove_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def query_rect_post(request):
    if request.method == 'POST':
        data = request.POST.dict()
        form = QueryRectForm(request.POST)
        if form.is_valid():
            item = " "
            for i in range(int(data['item_count'])):
                item += data[f"item{i+1}"] + " "
            query_txt = f"{request.session.get('token')} query {data['item_count']}{item}0 {form.cleaned_data['latitude1']} {form.cleaned_data['longitude1']} {form.cleaned_data['latitude2']} {form.cleaned_data['longitude2']} {form.cleaned_data['urgency']}"
            received = socket_service(query_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def query_circle_post(request):
    if request.method == 'POST':
        data = request.POST.dict()
        form = QueryCircleForm(request.POST)
        if form.is_valid():
            item = " "
            for i in range(int(data['item_count'])):
                item += data[f"item{i+1}"] + " "
            query_txt = f"{request.session.get('token')} query {data['item_count']}{item}1 {form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['radius']} {form.cleaned_data['urgency']}"
            received = socket_service(query_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def watch_rect_post(request):
    if request.method == 'POST':
        data = request.POST.dict()
        form = WatchRectForm(request.POST)
        if form.is_valid():
            item = " "
            for i in range(int(data['item_count'])):
                item += data[f"item{i+1}"] + " "
            watch_txt = f"{request.session.get('token')} watch {data['item_count']}{item}0 {form.cleaned_data['latitude1']} {form.cleaned_data['longitude1']} {form.cleaned_data['latitude2']} {form.cleaned_data['longitude2']} {form.cleaned_data['urgency']}"
            received = socket_service(watch_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def watch_circle_post(request):
    if request.method == 'POST':
        data = request.POST.dict()
        form = WatchCircleForm(request.POST)
        if form.is_valid():
            item = " "
            for i in range(int(data['item_count'])):
                item += data[f"item{i+1}"] + " "
            watch_txt = f"{request.session.get('token')} watch {data['item_count']}{item}1 {form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['radius']} {form.cleaned_data['urgency']}"
            received = socket_service(watch_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def unwatch_post(request):
    if request.method == 'POST':
        form = UnwatchForm(request.POST)
        if form.is_valid():
            unwatch_txt = request.session.get('token') + " unwatch " + form.cleaned_data['watch']
            received = socket_service(unwatch_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


# REQUEST POST PAGES
def mark_available_post(request):
    if request.method == 'POST':
        form = MarkAvailableForm(request.POST)
        if form.is_valid():
            mark_txt = f"{request.session.get('token')} mark_available {form.cleaned_data['request']} {form.cleaned_data['item']} {form.cleaned_data['amount']} {form.cleaned_data['expire']} {form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['comment']}"
            received = socket_service(mark_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def pick_post(request):
    if request.method == 'POST':
        form = PickForm(request.POST)
        if form.is_valid():
            pick_txt = f"{request.session.get('token')} pick {form.cleaned_data['request']} {form.cleaned_data['markavailable']} {form.cleaned_data['item']} {form.cleaned_data['amount']}"
            received = socket_service(pick_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def arrived_post(request):
    if request.method == 'POST':
        form = ArrivedForm(request.POST)
        if form.is_valid():
            arrived_txt = f"{request.session.get('token')} arrived {form.cleaned_data['request']} {form.cleaned_data['markavailable']}"
            received = socket_service(arrived_txt, test_socket)
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})

# POSTER METHOD
