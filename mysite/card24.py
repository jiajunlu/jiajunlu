# -*- coding: utf-8 -*-
"""
24

Created on Thu Oct 13 21:33:38 2016

@author: jiaju
"""

import itertools
import random
from collections import deque

# All possible ranks
cardranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

# All possible suits
cardsuits = ['of Clubs', 'of Diamonds', 'of Hearts', 'of Spades']

cardvalues = {'Ace': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
              '10': '10', 'Jack': '11', 'Queen': '12', 'King': '13'}

suitevalues = {'of Clubs': 0, 'of Diamonds': 1, 'of Hearts': 2, 'of Spades': 3}


def get_card_value(cardrank):
    return cardvalues[cardrank]


def get_card_index(cardrank, cardsuit):
    return int(get_card_value(cardrank)) + 13 * int(suitevalues[cardsuit])


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


def isOper(n):
    """
    >>> isOper('+')
    True
    >>> isOper('-')
    True
    >>> isOper('1')
    False
    >>> isOper(0)
    False
    """
    if n in ['+', '-', '*', '/']:
        return True
    return False


def get_all_possible_permutations(cardlist):
    num = len(cardlist)
    card_and_oper_list = []
    for x in itertools.product('+-*/', repeat=num-1):
        card_and_oper_list.append(tuple(cardlist) + x)
    return card_and_oper_list


def check_result(x_one):
    """it should in rear mode
    for example, 12*A+K- means 1*2+A-K

    >>> check_result('55+3*6-')
    True
    >>> check_result('55+3*5-')
    False
    >>> check_result('5+53*6-')
    False
    >>> check_result('+553*6-')
    False
    >>> check_result('55**36-')
    False
    >>> check_result(('1', '10', '3', '11', '*', '-', '-'))
    True
    """
    n1 = x_one[0]
    if isOper(n1):
        return False
    n2 = x_one[1]
    if isOper(n2):
        return False

    d = deque()
    d.append(n1)
    d.append(n2)

    num = len(x_one)
    for x in range(2, num):
        o = x_one[x]
        if isOper(o):
            try:
                n2 = d.pop()
                n1 = d.pop()
            except IndexError:
                return False
            if o == '/' and n2 == '0':
                return False
            if o == '/' and n2 == '0.0':
                return False
            temp = eval('(' + n1 + ')' + o + '(' + n2 + ')')
            if o == '/':
                temp1 = eval('(' + n1 + '*1.0)' + o + '(' + n2 + '*1.0)')
                if temp1 != temp:
                    return False
            d.append(str(temp))
        else:
            d.append(o)

    if len(d) == 1:
        answer = d.pop()
        if answer == '24':
            return True

    return False


def get_oper_weight(oper):
    if oper == '+':
        return 1
    elif oper == '-':
        return 2
    elif oper == '*':
        return 3
    elif oper == '/':
        return 4
    return 99


def print_result(x_one):
    """
    >>> print_result('55+3*6-')
    '(5+5)*3-6'
    >>> print_result(('1', '10', '3', '11', '*', '-', '-'))
    '1-(10-3*11)'
    >>> print_result(('1', '10', '3', '11', '/', '/', '-'))
    '1-10/(3/11)'
    >>> print_result(('1', '10', '3', '11', '-', '+', '-'))
    '1-(10+3-11)'
    """
    n1 = x_one[0]
    if isOper(n1):
        print ("Invalid")
        return
    n2 = x_one[1]
    if isOper(n2):
        print ("Invalid")
        return

    d = deque()
    d.append((n1, get_oper_weight(n1)))  # -3 means number
    d.append((n2, get_oper_weight(n2)))

    num = len(x_one)
    for x in range(2, num):
        o = x_one[x]
        if isOper(o):
            l = get_oper_weight(o)
            try:
                (n2, l2) = d.pop()
                (n1, l1) = d.pop()
            except IndexError:
                print ("Invalid")
                return
            if l1 == 1 or l1 == 2:  # + or -
                if l >= 3:      # * or /
                    n1 = '(' + n1 + ')'
            if l2 == 1 or l2 == 2:  # + or -
                if l >= 2:  # - or / or *  a-(b-c)
                    n2 = '(' + n2 + ')'
            if l2 == 4:
                if l == 4:  # a / ( b/c )
                    n2 = '(' + n2 + ')'
            temp = n1 + o + n2
            d.append((temp, l))
        else:
            d.append((o, 3))

    if len(d) == 1:
        (answer, l) = d.pop()
        return answer

    return ""


def get_24_answer(cards):
    answers = set()
    card_and_oper_list = get_all_possible_permutations(cards)
    for x in card_and_oper_list:
        x_all = itertools.permutations(x)
        for x_one in x_all:
            if check_result(x_one):
                pretty_one = print_result(x_one)
                if pretty_one in answers:
                    continue
                else:
                    answers.add(pretty_one)
                    print (pretty_one)
    return answers


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
