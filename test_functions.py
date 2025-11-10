out_cards={'kc' : 4} # key = out card (string), value = rank of hand type the card is for (int)
hole_cards={'kd':7,'jd':5}
com_cards={'kh':7,'ks':5,'6d':2}

# GIVEN FUNCTION: parse card string into (rank:int, suit:str)
def parse_card(card: str) -> tuple[int, str]:
    RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  't': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
    if len(card) != 2:
        raise ValueError(f"Invalid card string: {card}")
    r = card[0].lower()
    s = card[1].lower()
    if r not in RANK_ORDER:
        raise ValueError(f"Invalid rank: {r}")
    return (RANK_ORDER[r], s)

# slightly modified for test
def calculate_outs() -> dict:
    
    # add out-card to set (use inside hand type functions)
    def add_out(card: str, worth: int) -> None: # worth = rank assigned to each hand type
        in_set_greater = False;
        for key in out_cards:
            if key==card and worth < out_cards[key]:
                in_set_greater = True;
                # the existing card worth is greater, so doesn't update the set
                break;
        if in_set_greater == False:
            out_cards[card] = worth;
        return;


    # hand type functions:

    def four_of_a_kind() -> None:

        dealt_cards = set()
        # add player cards
        for card in hole_cards:
            if card:
                dealt_cards.add(card)
        # add community cards
        for card in com_cards:
            if card:
                dealt_cards.add(card)

        # store all seen ranks -> dealt_ranks
        dealt_ranks = []
        for card in dealt_cards:
            dealt_ranks.append(parse_card(card)[0])

        
        from collections import Counter
        # count each instance of seen ranks
        cnt = Counter(dealt_ranks)

        face_card = {10 : 't', 11 : 'j', 12 : 'q', 13 : 'k', 14 : 'a'} # in case rank is 10-13

        for rank_val, count in cnt.items():
            if count == 3:
                for suit in "hdsc":
                    if (rank_val in face_card): # if face card, change its rank to the name (eg 11 -> 'J')
                        card_to_add = f"{face_card[rank_val]}{suit}"
                    else:
                        card_to_add = f"{rank_val}{suit}"
                    if card_to_add not in dealt_cards:
                        add_out(card_to_add, 7)

    def full_house() -> None:
        pass

    def flush() -> None:
        pass

    def straight() -> None:
        pass

    def three_of_a_kind() -> None:
        pass

    def two_pairs() -> None:
        pass

    def high_pair() -> None:
        pass

    def low_pair() -> None:
        pass


    # find all outs

    four_of_a_kind();
    full_house();
    flush();
    straight();
    three_of_a_kind();
    two_pairs();
    high_pair();
    low_pair();

    return out_cards;


out_cards = calculate_outs()
print(out_cards)