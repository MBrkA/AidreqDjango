from django.http import HttpResponse
from django.shortcuts import render, redirect

from front.forms import *
from front.socket import DjangoSocket

import threading

mutex = threading.Lock()
cond = threading.Condition(mutex)
socket = DjangoSocket()
socket.start()

# Create your views here.


def main(request):
    if request.session.get("token", False):
        campaign = request.session.get("campaign", False)
        return redirect('/home', {'campaign': campaign})

    form = LoginForm()
    return redirect('/login', {'form': form})


def home(request):
    if not request.session.get("token", False):
        campaign = request.session.get("campaign", False)
        return redirect('/login')
    campaign = request.session.get("campaign", False)
    return render(request, 'home.html', {'campaign': campaign})


def login_post(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        with socket.cond:
            socket.send_q.put("login " + form.cleaned_data["username"] + " " + form.cleaned_data["password"])
            received = socket.recv_q.get()
        if "Login successful" in received:
            request.session["token"] = received.split(" ")[2]
            campaign = request.session.get("campaign", False)
            return redirect('/home', {'campaign': campaign})
        else:
            return render(request, 'form_page.html', {'form': form, 'title': 'Login', 'action': 'login_post'})
    else:
        return render(request, 'form_page.html', {'form': form, 'title': 'Login', 'action': 'login_post'})


def login(request):
    form = LoginForm(request.GET)
    return render(request, 'form_page.html', {'form': form, 'title': 'Login', 'action': 'login_post'})


def logout(request):
    with socket.cond:
        socket.send_q.put("logout")
        received = socket.recv_q.get()
    if "Logout successful" in received:
        request.session.flush()
    return redirect('/login')


def logout_post(request):
    with socket.cond:
        socket.send_q.put("logout")
        received = socket.recv_q.get()
    if "Logout successful" in received:
        request.session.flush()
    return redirect('/login')

#################################
#  FORM PAGES
#################################


# CAMPAIGN FORM PAGES
def create_campaign(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = CreateCampaignForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Create Campaign', 'action': 'create_campaign_post'})


def list_campaigns(request):
    if not request.session.get("token", False):
        return redirect('/login')
    with socket.cond:
        socket.send_q.put("list")
        received = socket.recv_q.get()
    if "##EOF##" in received:
        received = received.replace("##EOF##", "")
    campaigns = received.split("\t")
    return render(request, 'result.html', {'result': campaigns})


def open_campaign(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = OpenCampaignForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Open Campaign', 'action': 'open_campaign_post'})


def close_campaign(request):
    create_txt = "close"
    with socket.cond:
        socket.send_q.put(create_txt)
        received = socket.recv_q.get()
    del request.session["campaign"]
    return render(request, 'result.html', {'result': received})


# ITEMS FORM PAGES
def search_item(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = SearchItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Search Item', 'action': 'search_item_post'})


def get_all_items(request):
    if not request.session.get("token", False):
        return redirect('/login')


def update_item(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = UpdateItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Update Item', 'action': 'update_item_post'})


def delete_item(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = RemoveItemForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Delete Item', 'action': 'delete_item_post'})


# CAMPAIGN OPERATIONS FORM PAGES
def add_request(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = AddRequestForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Add Request', 'action': 'add_request_post'})


def get_all_requests(request):
    if not request.session.get("token", False):
        return redirect('/login')
    with socket.cond:
        socket.send_q.put("get_all_requests")
        received = socket.recv_q.get()
    requests = received.split("\n")
    return render(request, 'result.html', {'result': requests, 'title': 'All Requests In Campaign'})


def get_request(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = GetRequestForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Get Request', 'action': 'get_request_post'})


def update_request(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = UpdateRequestForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Update Request', 'action': 'update_request_post'})


def remove_request(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = RemoveRequestForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Remove Request', 'action': 'remove_request_post'})


def query_rect(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = QueryRectForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Query Rect', 'action': 'query_rect_post'})


def query_circle(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = QueryCircleForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Query Circle', 'action': 'query_circle_post'})


def watch_rect(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = WatchRectForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Watch Rect', 'action': 'watch_rect_post'})


def watch_circle(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = WatchCircleForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Watch Circle', 'action': 'watch_circle_post'})


def unwatch(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = UnwatchForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Unwatch', 'action': 'unwatch_post'})


# REQUEST FORM PAGES
def mark_available(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = MarkAvailableForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Mark Available', 'action': 'mark_available_post'})


def pick(request):
    if not request.session.get("token", False):
        return redirect('/login')
    form = PickForm()
    return render(request, 'form_page.html', {'form': form, 'title': 'Pick', 'action': 'pick_post'})


def arrived(request):
    if not request.session.get("token", False):
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
            search_txt = "search_item " + form.cleaned_data['name']
            with socket.cond:
                socket.send_q.put(search_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def get_all_items_post(request):
    return render(request, 'result.html', {'result': "Invalid request"})


def update_item_post(request):
    if request.method == 'POST':
        form = UpdateItemForm(request.POST)
        if form.is_valid():
            update_txt = f"update_item {form.cleaned_data['target']} {form.cleaned_data['name']} {form.cleaned_data['synonyms']}"
            with socket.cond:
                socket.send_q.put(update_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def delete_item_post(request):
    if request.method == 'POST':
        form = RemoveItemForm(request.POST)
        if form.is_valid():
            delete_txt = "remove_item " + form.cleaned_data['name']
            with socket.cond:
                socket.send_q.put(delete_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


# CAMPAIGN POST PAGES
def create_campaign_post(request):
    if request.method == 'POST':
        form = CreateCampaignForm(request.POST)
        if form.is_valid():
            create_txt = f"new {form.cleaned_data['name']} {form.cleaned_data['description']}"
            with socket.cond:
                socket.send_q.put(create_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    else:
        return render(request, 'result.html', {'result': "Invalid request"})


def open_campaign_post(request):
    if request.method == 'POST':
        form = OpenCampaignForm(request.POST)
        if form.is_valid():
            open_txt = "open " + form.cleaned_data['name']
            with socket.cond:
                socket.send_q.put(open_txt)
                received = socket.recv_q.get()
            request.session["campaign"] = form.cleaned_data['name']
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    else:
        return render(request, 'result.html', {'result': "Invalid request"})


def add_request_post(request):
    if request.method == 'POST':
        form = AddRequestForm(request.POST)
        if form.is_valid():
            add_txt = f"add_request {form.cleaned_data['item']} {form.cleaned_data['amount']} {form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['urgency']} {form.cleaned_data['description']}"
            with socket.cond:
                socket.send_q.put(add_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def get_request_post(request):
    if request.method == 'POST':
        form = GetRequestForm(request.POST)
        if form.is_valid():
            get_txt = "get_request " + form.cleaned_data['request']
            with socket.cond:
                socket.send_q.put(get_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def update_request_post(request):
    if request.method == 'POST':
        form = UpdateRequestForm(request.POST)
        if form.is_valid():
            update_txt = f"update_request {form.cleaned_data['request']} {form.cleaned_data['item']} {form.cleaned_data['amount']} {form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['urgency']} {form.cleaned_data['description']}"
            with socket.cond:
                socket.send_q.put(update_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def remove_request_post(request):
    if request.method == 'POST':
        form = RemoveRequestForm(request.POST)
        if form.is_valid():
            remove_txt = "remove_request " + form.cleaned_data['request']
            with socket.cond:
                socket.send_q.put(remove_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def query_rect_post(request):
    if request.method == 'POST':
        form = QueryRectForm(request.POST)
        if form.is_valid():
            query_txt = f"query {form.cleaned_data['item']} 0 {form.cleaned_data['latitude1']} {form.cleaned_data['longitude1']} {form.cleaned_data['latitude2']} {form.cleaned_data['longitude2']} {form.cleaned_data['urgency']}"
            with socket.cond:
                socket.send_q.put(query_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def query_circle_post(request):
    if request.method == 'POST':
        form = QueryCircleForm(request.POST)
        if form.is_valid():
            query_txt = f"query {form.cleaned_data['item']} 1 {form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['radius']} {form.cleaned_data['urgency']}"
            with socket.cond:
                socket.send_q.put(query_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def watch_rect_post(request):
    if request.method == 'POST':
        form = WatchRectForm(request.POST)
        if form.is_valid():
            watch_txt = f"watch {form.cleaned_data['item']} 0 {form.cleaned_data['latitude1']} {form.cleaned_data['longitude1']} {form.cleaned_data['latitude2']} {form.cleaned_data['longitude2']} {form.cleaned_data['urgency']}"
            with socket.cond:
                socket.send_q.put(watch_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def watch_circle_post(request):
    if request.method == 'POST':
        form = WatchCircleForm(request.POST)
        if form.is_valid():
            watch_txt = f"watch {form.cleaned_data['item']} 1 {form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['radius']} {form.cleaned_data['urgency']}"
            with socket.cond:
                socket.send_q.put(watch_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def unwatch_post(request):
    if request.method == 'POST':
        form = UnwatchForm(request.POST)
        if form.is_valid():
            unwatch_txt = "unwatch " + form.cleaned_data['watch']
            with socket.cond:
                socket.send_q.put(unwatch_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


# REQUEST POST PAGES
def mark_available_post(request):
    if request.method == 'POST':
        form = MarkAvailableForm(request.POST)
        if form.is_valid():
            mark_txt = f"mark_available {form.cleaned_data['request']} {form.cleaned_data['item']} {form.cleaned_data['amount']} {form.cleaned_data['expire']} {form.cleaned_data['latitude']} {form.cleaned_data['longitude']} {form.cleaned_data['comment']}"
            with socket.cond:
                socket.send_q.put(mark_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def pick_post(request):
    if request.method == 'POST':
        form = PickForm(request.POST)
        if form.is_valid():
            pick_txt = f"pick {form.cleaned_data['request']} {form.cleaned_data['markavailable']} {form.cleaned_data['item']} {form.cleaned_data['amount']}"
            with socket.cond:
                socket.send_q.put(pick_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})


def arrived_post(request):
    if request.method == 'POST':
        form = ArrivedForm(request.POST)
        if form.is_valid():
            arrived_txt = f"arrived {form.cleaned_data['request']} {form.cleaned_data['markavailable']}"
            with socket.cond:
                socket.send_q.put(arrived_txt)
                received = socket.recv_q.get()
            return render(request, 'result.html', {'result': received})
        else:
            return render(request, 'result.html', {'result': "Invalid form"})
    return render(request, 'result.html', {'result': "Invalid request"})

# POSTER METHOD
