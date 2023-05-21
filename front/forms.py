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

class CloseCampaignForm(forms.Form):
    name = forms.CharField(label='name', max_length=64, required=True)
