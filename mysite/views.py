from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from card24 import get_24_answer
from card24 import random_choose_4_cards
from card24 import get_card_value


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
    today_cards = random_choose_4_cards()
    card_urls = []
    cards_dict = {}

    if request.method == 'POST':
        cards = Card24Form(request.POST)
        if cards.is_valid():
            c1 = cards.cleaned_data['c1']
            c2 = cards.cleaned_data['c2']
            c3 = cards.cleaned_data['c3']
            c4 = cards.cleaned_data['c4']
            result = get_24_answer([c1, c2, c3, c4])
    else:
        cards = []
        for card in today_cards:
            c, s = card
            card_url = "/static/img/" + str(c) + " " + s + ".png"
            card_url = card_url.lower()
            card_url = card_url.replace(" ", "_")
            card_urls.append(card_url)
            cards.append(c)
        cards_dict['c1'] = get_card_value(cards[0])
        cards_dict['c2'] = get_card_value(cards[1])
        cards_dict['c3'] = get_card_value(cards[2])
        cards_dict['c4'] = get_card_value(cards[3])
        card_form = Card24Form(initial=cards_dict)

    return render(request, 'card24.html', {'cards': card_urls, 'form': card_form, 'result': result})
