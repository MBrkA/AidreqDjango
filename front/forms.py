from django import forms

## LOGIN FORM
class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=64, required=True)
    password = forms.CharField(label='password', widget=forms.PasswordInput(), required=True)

## ITEMS FORMS
class SearchItemForm(forms.Form):
    name = forms.CharField(label='name', max_length=64, required=True)

class UpdateItemForm(forms.Form):
    target = forms.CharField(label='target', max_length=64, required=True)
    name = forms.CharField(label='name', max_length=64, required=False)
    synonyms = forms.CharField(widget=forms.Textarea, label='synonyms', required=False)

class RemoveItemForm(forms.Form):
    name = forms.CharField(label='name', max_length=64, required=True)

## CAMPAIGN FORMS
class CreateCampaignForm(forms.Form):
    name = forms.CharField(label='name', max_length=64, required=True)
    description = forms.CharField(widget=forms.Textarea, label='description', required=False)

class OpenCampaignForm(forms.Form):
    name = forms.CharField(label='name', max_length=64, required=True)

class AddRequestForm(forms.Form):
    item = forms.CharField(label='item', max_length=64, required=True)
    amount = forms.IntegerField(label='quantity', required=True)
    latitude = forms.FloatField(label='latitude', required=True)
    longitude = forms.FloatField(label='longitude', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='urgency', required=True)
    description = forms.CharField(widget=forms.Textarea, label='description', required=False)

class GetRequestForm(forms.Form):
    request = forms.CharField(label='requestid', max_length=64, required=True)

class UpdateRequestForm(forms.Form):
    request = forms.CharField(label='requestid', max_length=64, required=True)
    item = forms.CharField(label='item', max_length=64, required=False)
    amount = forms.IntegerField(label='quantity', required=False)
    latitude = forms.FloatField(label='latitude', required=False)
    longitude = forms.FloatField(label='longitude', required=False)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='urgency', required=False)
    description = forms.CharField(widget=forms.Textarea, label='description', required=False)

class RemoveRequestForm(forms.Form):
    request = forms.CharField(label='requestid', max_length=64, required=True)

class QueryRectForm(forms.Form):
    item = forms.CharField(label='item', max_length=64, required=True)
    latitude1 = forms.FloatField(label='latitude1', required=True)
    longitude1 = forms.FloatField(label='longitude1', required=True)
    latitude2 = forms.FloatField(label='latitude2', required=True)
    longitude2 = forms.FloatField(label='longitude2', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='urgency', required=True)

class QueryCircleForm(forms.Form):
    item = forms.CharField(label='item', max_length=64, required=True)
    latitude = forms.FloatField(label='latitude', required=True)
    longitude = forms.FloatField(label='longitude', required=True)
    radius = forms.FloatField(label='radius', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='urgency', required=True)

class WatchRectForm(forms.Form):
    item = forms.CharField(label='item', max_length=64, required=True)
    latitude1 = forms.FloatField(label='latitude1', required=True)
    longitude1 = forms.FloatField(label='longitude1', required=True)
    latitude2 = forms.FloatField(label='latitude2', required=True)
    longitude2 = forms.FloatField(label='longitude2', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='urgency', required=True)

class WatchCircleForm(forms.Form):
    item = forms.CharField(label='item', max_length=64, required=True)
    latitude = forms.FloatField(label='latitude', required=True)
    longitude = forms.FloatField(label='longitude', required=True)
    radius = forms.FloatField(label='radius', required=True)
    urgency = forms.CharField(widget=forms.Select(choices=[('URGENT', 'URGENT'), ('SOON', 'SOON'), ('DAYS', 'DAYS'), ('WEEKS','WEEKS'), ('OPTIONAL','OPTIONAL')]), label='urgency', required=True)

class UnwatchForm(forms.Form):
    watch = forms.CharField(label='watchid', max_length=64, required=True)


## REQUEST FORMS
class MarkAvailableForm(forms.Form):
    request = forms.CharField(label='requestid', max_length=64, required=True)
    item = forms.CharField(label='item', max_length=64, required=True)
    amount = forms.IntegerField(label='quantity', required=True)
    expire = forms.IntegerField(label='expire', required=True)
    latitude = forms.FloatField(label='latitude', required=True)
    longitude = forms.FloatField(label='longitude', required=True)
    comment = forms.CharField(widget=forms.Textarea, label='comment', required=False)

class PickForm(forms.Form):
    request = forms.CharField(label='requestid', max_length=64, required=True)
    markavailable = forms.CharField(label='markavailableid', max_length=64, required=True)
    item = forms.CharField(label='item', max_length=64, required=True)
    amount = forms.IntegerField(label='quantity', required=True)

class ArrivedForm(forms.Form):
    request = forms.CharField(label='requestid', max_length=64, required=True)
    markavailable = forms.CharField(label='markavailableid', max_length=64, required=True)