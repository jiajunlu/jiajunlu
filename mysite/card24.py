# -*- coding: utf-8 -*-
"""
24

Created on Thu Oct 13 21:33:38 2016

@author: jiaju
"""

import itertools
import random
from collections import deque
from operator import mul, sub, add


def div(a, b):
    if b == 0:
        return 999999.0
    return a / b
 
ops = {mul: '*', div: '/', sub: '-', add: '+'}

# All possible ranks
cardranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

# All possible suits
cardsuits = ['of Clubs', 'of Diamonds', 'of Hearts', 'of Spades']

cardvalues = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13}

suitevalues = {'of Clubs': 0, 'of Diamonds': 1, 'of Hearts': 2, 'of Spades': 3}


def get_card_value(cardrank):
    return cardvalues[cardrank]


def get_card_index(cardrank, cardsuit):
    return get_card_value(cardrank) + 13 * int(suitevalues[cardsuit])


def get_card_from_index(index):
    rank = index % 13
    if rank == 0:
        rank = 13
    rank = rank - 1
    return (cardranks[rank], cardsuits[(index-1)/13])


def get_card_value_from_index(index):
    v = index % 13
    if v == 0:
        return 13
    return v


def random_choose_4_cards():
    deck = list(itertools.product(cardranks, cardsuits))
    random.shuffle(deck)
    four_cards = []
    for i in range(4):
        rank, suit = deck[i]
        four_cards.append((rank, suit))
    return four_cards


def solve24(num, how, target):
    if len(num) == 1:
        if round(num[0], 5) == round(target, 5):
            yield str(how[0]).replace(',', '').replace("'", '')
    else:
        for i, n1 in enumerate(num):
            for j, n2 in enumerate(num):
                if i != j:
                    for op in ops:
                        new_num = [n for k, n in enumerate(num) if k != i and k != j] + [op(n1, n2)]
                        new_how = [h for k, h in enumerate(how) if k != i and k != j] + [(how[i], ops[op], how[j])]
                        yield from solve24(new_num, new_how, target)


def get_24_answer(cards):
    answers = set()
    nums = [c for c in cards]
    for n in solve24(nums, nums, 24):
        answers.add(n)
    return answers


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

