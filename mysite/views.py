from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from mysite.card24 import get_24_answer
from mysite.card24 import random_choose_4_cards
from mysite.card24 import get_card_value_from_index
from mysite.card24 import get_card_index
from mysite.models import Card24Game
from mysite.models import Card24Game_SavedAnswer


class Card24Form(forms.Form):
    c1 = forms.CharField(label="1st card", widget=forms.TextInput)
    c2 = forms.CharField(label="2nd card", widget=forms.TextInput)
    c3 = forms.CharField(label="3rd card", widget=forms.TextInput)
    c4 = forms.CharField(label="4th card", widget=forms.TextInput)

# Create your views here.


def index(request):
    return HttpResponse("Home")


def card24_querycache(question):
    '''
    question is a list of card values ['1', '13', '12', '2']
    '''
    try:
        question = sorted(question)
        incache = Card24Game_SavedAnswer.objects.get(question=question)
        if incache:
            queryset = Card24Game.objects.filter(question=question)
            return (True, [q.answer for q in queryset])
        else:
            return (True, [])
    except Card24Game_SavedAnswer.DoesNotExist:
        return (False, [])


def card24_savequestion(question, answers):
    # query cache again
    try:
        Card24Game_SavedAnswer.objects.get(question=question)
        return
    except Card24Game_SavedAnswer.DoesNotExist:
        question = sorted(question)
        if len(answers) > 0:
            c = Card24Game_SavedAnswer(question=question, incache=True)
            c.save()
            for a in answers:
                a = Card24Game(question=question, answer=a)
                a.save()
        else:
            c = Card24Game_SavedAnswer(question=question, incache=False)
            c.save()


def card24_getdict(c1, c2, c3, c4):
    cards_dict = {}
    cards_dict['c1'] = c1
    cards_dict['c2'] = c2
    cards_dict['c3'] = c3
    cards_dict['c4'] = c4
    return cards_dict


def card24_get_answer_from_value(c1, c2, c3, c4):
    result = []
    question = sorted([c1, c2, c3, c4])
    (incache, answers) = card24_querycache(question)
    if incache:
        result = answers
    else:
        result = get_24_answer(question)
        card24_savequestion(question, result)
    return result


def card24_get_answer_from_cards(c1, c2, c3, c4):
    return card24_get_answer_from_value(str(get_card_value_from_index(int(c1))),
                                        str(get_card_value_from_index(int(c2))),
                                        str(get_card_value_from_index(int(c3))),
                                        str(get_card_value_from_index(int(c4))))


def card24_get_answer(today_cards):
    cards = []
    for card in today_cards:
        c, s = card
        cards.append(get_card_index(c, s))
    return card24_get_answer_from_value(str(get_card_value_from_index(int(cards[0]))),
                                        str(get_card_value_from_index(int(cards[1]))),
                                        str(get_card_value_from_index(int(cards[2]))),
                                        str(get_card_value_from_index(int(cards[3]))))


def card24_get_card_urls(today_cards):
    card_urls = []
    for card in today_cards:
        c, s = card
        card_url = str(c) + " " + s
        card_url = card_url.lower()
        card_url = card_url.replace(" ", "_")
        card_urls.append(card_url)
    return card_urls


def card24(request):
    card_form = Card24Form()
    result = ""
    card_urls = []
    input_cards = ""
    yesnoanswer = ""
    today_cards = []

    if request.method == 'POST':
        if request.POST.get("yesnoanswer") or request.POST.get("fullanswer"):
            today_cards = request.session['cards']
            result = card24_get_answer(today_cards)
            if request.POST.get("yesnoanswer"):
                if len(result) > 0:
                    yesnoanswer = "yes"
                else:
                    yesnoanswer = "no"
                input_cards = ""
            else:
                x = ", ".join(["%s" % k for (k, v) in today_cards])
                input_cards = "Cards: " + x
            card_urls = card24_get_card_urls(today_cards)
        else:
            cards = Card24Form(request.POST)
            if cards.is_valid():
                c1 = cards.cleaned_data['c1']
                c2 = cards.cleaned_data['c2']
                c3 = cards.cleaned_data['c3']
                c4 = cards.cleaned_data['c4']
                input_cards = "Cards: " + c1 + ", " + c2 + ", " + c3 + ", " + c4 + ":"
                result = card24_get_answer_from_cards(c1, c2, c3, c4)
                yesnoanswer = ""
    else:
        today_cards = random_choose_4_cards()
        request.session['cards'] = today_cards
        card_urls = card24_get_card_urls(today_cards)

    return render(request, 'card24.html', {'input_cards': input_cards,
                                           'cards': card_urls,
                                           'form': card_form,
                                           'yesnoanswer': yesnoanswer,
                                           'result': result})
