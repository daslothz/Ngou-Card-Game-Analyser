#!/usr/bin/env python
# coding: utf-8

# # Cow analyzer

# * Analyses the best combination of base (3 cards) + points (2 cards)



from itertools import combinations


# ## Helper functions

# * switch



""" def switch(hand):
    for i in range(len(hand)):
        if int(hand[i]) in [3, 6]:
            hand[i] = "switch"
    return hand
 """


# ** EDIT
# 
# - Move all 3s and 6s to the start of the pile
# - Initialise a counter (number of 3s and 6s) that also acts as a pointer to the 3s and 6s




def switch2(hand):
    switches = []
    others = []
    for i in range(len(hand)):
        if str(hand[i]) in ['3', '6'] or hand[i] in [3, 6]:
            switches.append(hand[i])
        else:
            others.append(hand[i])
    res = switches + others
    count36 = len(switches)
    return res, count36


# * Card value




def card_value(card):
    if card in ['J','Q','K']:
        return 10
    elif card == 'A':
        return 1
    else:
        return int(card)


# * base sum




def base_sum(hand):
    newHand, count36 = switch2(hand)
    combos = []
    for combo in combinations(newHand, 3):
        numbers = []
        switches_in_combo = 0
        for card in combo:
            if card in ['J', 'Q', 'K', 'A']:
                numbers.append(card_value(card))
            elif card in [3, 6]:
                switches_in_combo += 1
            else:
                numbers.append(card_value(card))
        sums = []
        base_sum_value = sum(numbers)
        if switches_in_combo == 1:
            sums.append(base_sum_value + 3)
            sums.append(base_sum_value + 6)
        elif switches_in_combo == 2:
            sums.append(base_sum_value + 3 + 3)
            sums.append(base_sum_value + 3 + 6)
            sums.append(base_sum_value + 6 + 6)
        elif switches_in_combo == 3:
            sums.append(base_sum_value + 3 + 3 + 3)
            sums.append(base_sum_value + 3 + 3 + 6)
            sums.append(base_sum_value + 3 + 6 + 6)
            sums.append(base_sum_value + 6 + 6 + 6)
        else:
            sums.append(base_sum_value)
        for v in sums:
            if v % 10 == 0:
                combos.append(combo)
                break  
    return combos





# * Points for the last 2 cards




def score_points(pair):
    numbers = []
    switch_count = 0
    for card in pair:
        if card in ['J','Q','K','A']:
            numbers.append(card_value(card))
        elif card == 3 or card == 6:
            switch_count += 1
        else:
            numbers.append(card_value(card))
    possible_scores = []
    if switch_count == 0:
        possible_scores.append(sum(numbers) % 10)
    elif switch_count == 1:
        possible_scores.append((numbers[0]+3)%10)
        possible_scores.append((numbers[0]+6)%10)
    elif switch_count == 2:
        possible_scores.append((3+3 + numbers[0]) %10 if numbers else 6)
        possible_scores.append((3+6 + numbers[0]) %10 if numbers else 9)
        possible_scores.append((6+6 + numbers[0]) %10 if numbers else 2)
    return max(possible_scores)


# ## Combo maker




def validcombos(hand):
    combos = {} # key = list containing the cards making up base 10, val = final 2 cards
    base10s = base_sum(hand)
    if len(base10s) == 0:
        print("No base 10, better luck next time!")
    seen = {}
    for base in base10s:
        temp = hand.copy()
        for card in base:
            temp.remove(card)
        base_fset = frozenset(base) # immutable set -- comparing elements but do not care about order (cannot use tup or ls here as they are order sensitive)
        if base_fset not in seen:
            seen[base_fset] = True      
            combos[base] = temp          
    return combos





# ## Main


def normalize(hand):
    out = []
    for x in hand:
        if isinstance(x, str) and x.isdigit():
            out.append(int(x))
        else:
            out.append(x)
    return out

# returns all combo
def cow(hand, mushroom):
    hand = [int(x) if isinstance(x, str) and x.isdigit() else x for x in hand]
    hand = normalize(hand)
    combos = validcombos(hand)
    best_rank = -1
    best_points = -1
    best_base = None
    best_score = None
    for base, score in combos.items():
        if 'A' in score and mushroom and any(x in score for x in ['J','Q','K']):
            return f"Base:{base} \nScore:{score}, \nDong Gu"
        elif score[0] == score[1] and score[0] != 'switch':
            rank = 3
            val = card_value(score[0])
        else:
            val = score_points(score)
            if val == 0:
                rank = 2
            else:
                rank = 1
        if rank > best_rank or (rank == best_rank and val > best_points):
            best_rank = rank
            best_points = val
            best_base = base
            best_score = score
    if best_rank == 3:
        return f"Base: {best_base}, \nScore: {best_score}, \nOne Pair"
    elif best_rank == 2:
        return f"Base: {best_base}, \nScore: {best_score}, \n10 Points"
    else:
        return f"Base: {best_base}, \nScore: {best_score}, \nPoints: {best_points}"



