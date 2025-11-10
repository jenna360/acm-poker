out_cards={'6c':7}
hole_cards=['5h','ac']
com_cards=['7c','2c','jh','3c']

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

    # to keep track of all cards we can see
    dealt_cards = set()
    # add player cards
    for card in hole_cards:
        if card:
            dealt_cards.add(card)
    # add community cards
    for card in com_cards:
        if card:
            dealt_cards.add(card)

    # hand type functions:

    def four_of_a_kind() -> None:
        pass

    def full_house() -> None:
        pass

    def flush() -> None:
        # store dealt cards (str) in lists based on suit
        dealt_suits = {'h':[],'c':[],'d':[],'s':[]};
        for card in dealt_cards:
            dealt_suits[parse_card(card)[1].lower()].append(card);
    
        for suit in dealt_suits: # finds the cards necessary to make a flush of this suit
            if len(dealt_suits[suit])==4:
                ranks = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:'t', 11:'j', 12:'q', 13:'k', 14:'a'};
                for card in dealt_suits[suit]: # remove rank from possible out-card ranks
                    ranks.pop(parse_card(card)[0]);
                for r in ranks:
                    add_out(f"{ranks[r]}{suit}",5);

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