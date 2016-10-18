from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from card24 import get_24_answer


class Card24Form(forms.Form):
    c1 = forms.CharField(label="1st card", widget=forms.TextInput)
    c2 = forms.CharField(label="2nd card", widget=forms.TextInput)
    c3 = forms.CharField(label="3rd card", widget=forms.TextInput)
    c4 = forms.CharField(label="4th card", widget=forms.TextInput)

# Create your views here.


def index(request):
    return HttpResponse("Home")


def card24(request):
    card_form = Card24Form()
    result = ""
    if request.method == 'POST':
        cards = Card24Form(request.POST)
        if cards.is_valid():
            c1 = cards.cleaned_data['c1']
            c2 = cards.cleaned_data['c2']
            c3 = cards.cleaned_data['c3']
            c4 = cards.cleaned_data['c4']
            result = get_24_answer([c1, c2, c3, c4])
    return render(request, 'card24.html', {'form': card_form, 'result': result})
