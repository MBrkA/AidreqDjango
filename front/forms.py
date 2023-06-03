from django import forms


# LOGIN FORM
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True)


# ITEMS FORMS
class SearchItemForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64, required=True)


class UpdateItemForm(forms.Form):
    target = forms.CharField(label='Target', max_length=64, required=True)
    name = forms.CharField(label='Name', max_length=64, required=True)
    synonyms = forms.CharField(widget=forms.Textarea, label='Synonyms', required=True)


class RemoveItemForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64, required=True)


# CAMPAIGN FORMS
class CreateCampaignForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64, required=True)
    description = forms.CharField(widget=forms.Textarea, label='Description', required=True)


class OpenCampaignForm(forms.Form):
    name = forms.CharField(widget=forms.Select(choices=[]), label='Campaign', required=True)
    #name = forms.CharField(label='Name', max_length=64, required=True)


class AddRequestForm(forms.Form):
    latitude = forms.FloatField(label='Latitude', required=True)
    longitude = forms.FloatField(label='Longitude', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='Urgency', required=True)
    description = forms.CharField(widget=forms.Textarea, label='Description', required=True)


class GetAllRequestsForm(forms.Form):
    campaign = forms.CharField(label='campaign', max_length=64, required=True)

class GetRequestForm(forms.Form):
    request = forms.CharField(widget=forms.Select(choices=[]), label='Request', required=True)

class UpdateRequestForm(forms.Form):
    request = forms.CharField(widget=forms.Select(choices=[]), label='Request', required=True)
    #request = forms.CharField(label='requestid', max_length=64, required=True)
    latitude = forms.FloatField(label='Latitude', required=True)
    longitude = forms.FloatField(label='Longitude', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='Urgency', required=True)
    description = forms.CharField(widget=forms.Textarea, label='Description', required=True)


class RemoveRequestForm(forms.Form):
    request = forms.CharField(widget=forms.Select(choices=[]), label='Request', required=True)


class QueryRectForm(forms.Form):
    latitude1 = forms.FloatField(label='Latitude1', required=True)
    longitude1 = forms.FloatField(label='Longitude1', required=True)
    latitude2 = forms.FloatField(label='Latitude2', required=True)
    longitude2 = forms.FloatField(label='Longitude2', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='Urgency', required=True)


class QueryCircleForm(forms.Form):
    latitude = forms.FloatField(label='Latitude', required=True)
    longitude = forms.FloatField(label='Longitude', required=True)
    radius = forms.FloatField(label='Radius', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='Urgency', required=True)


class WatchRectForm(forms.Form):
    latitude1 = forms.FloatField(label='Latitude1', required=True)
    longitude1 = forms.FloatField(label='Longitude1', required=True)
    latitude2 = forms.FloatField(label='Latitude2', required=True)
    longitude2 = forms.FloatField(label='Longitude2', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='Urgency', required=True)


class WatchCircleForm(forms.Form):
    latitude = forms.FloatField(label='Latitude', required=True)
    longitude = forms.FloatField(label='Longitude', required=True)
    radius = forms.FloatField(label='Radius', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='Urgency', required=True)


class UnwatchForm(forms.Form):
    watch = forms.CharField(label='Watchid', max_length=64, required=True)


# REQUEST FORMS
class MarkAvailableForm(forms.Form):
    request = forms.CharField(label='Requestid', max_length=64, required=True)
    item = forms.CharField(label='Item', max_length=64, required=True)
    amount = forms.IntegerField(label='Amount', required=True)
    expire = forms.IntegerField(label='Expire(hours)', required=True)
    latitude = forms.FloatField(label='Latitude', required=True)
    longitude = forms.FloatField(label='Longitude', required=True)
    comment = forms.CharField(widget=forms.Textarea, label='Comment', required=True)


class PickForm(forms.Form):
    request = forms.CharField(label='RequestId', max_length=64, required=True)
    markavailable = forms.CharField(label='MarkavailableId', max_length=64, required=True)
    item = forms.CharField(label='Item', max_length=64, required=True)
    amount = forms.IntegerField(label='Amount', required=True)


class ArrivedForm(forms.Form):
    request = forms.CharField(label='RequestId', max_length=64, required=True)
    markavailable = forms.CharField(label='MarkAvailableId', max_length=64, required=True)