from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from card24 import get_24_answer
from card24 import random_choose_4_cards
from card24 import get_card_value
from models import Card24Game
from models import Card24Game_SavedAnswer


class Card24Form(forms.Form):
    c1 = forms.CharField(label="1st card", widget=forms.TextInput)
    c2 = forms.CharField(label="2nd card", widget=forms.TextInput)
    c3 = forms.CharField(label="3rd card", widget=forms.TextInput)
    c4 = forms.CharField(label="4th card", widget=forms.TextInput)

# Create your views here.


def index(request):
    return HttpResponse("Home")


def card24_querycache(question):
    try:
        incache = Card24Game_SavedAnswer.objects.get(question=question)
        if incache:
            queryset = Card24Game.objects.filter(question=question)
            return (True, [q.answer for q in queryset])
        else:
            return (True, [])
    except Card24Game_SavedAnswer.DoesNotExist:
        return (False, [])


def card24_savequestion(question, answers):
    if len(answers) > 0:
        c = Card24Game_SavedAnswer(question=question, incache=True)
        c.save()
        for a in answers:
            a = Card24Game(question=question, answer=a)
            a.save()
    else:
        c = Card24Game_SavedAnswer(question=question, incache=False)
        c.save()


def card24(request):
    card_form = Card24Form()
    result = ""
    today_cards = random_choose_4_cards()
    card_urls = []
    cards_dict = {}
    input_cards = ""

    if request.method == 'POST':
        cards = Card24Form(request.POST)
        if cards.is_valid():
            c1 = cards.cleaned_data['c1']
            c2 = cards.cleaned_data['c2']
            c3 = cards.cleaned_data['c3']
            c4 = cards.cleaned_data['c4']
            question = sorted([c1, c2, c3, c4])
            (incache, answers) = card24_querycache(question)
            if incache:
                result = answers
            else:
                result = get_24_answer(question)
                card24_savequestion(question, result)
            input_cards = "Card: " + c1 + ', ' + c2 + ', ' + c3 + ', ' + c4

    cards = []
    for card in today_cards:
        c, s = card
        card_url = str(c) + " " + s
        card_url = card_url.lower()
        card_url = card_url.replace(" ", "_")
        card_urls.append(card_url)
        cards.append(c)
    cards_dict['c1'] = get_card_value(cards[0])
    cards_dict['c2'] = get_card_value(cards[1])
    cards_dict['c3'] = get_card_value(cards[2])
    cards_dict['c4'] = get_card_value(cards[3])
    card_form = Card24Form(initial=cards_dict)

    return render(request, 'card24.html', {'input_cards': input_cards,
                                           'cards': card_urls,
                                           'form': card_form, 'result': result})
