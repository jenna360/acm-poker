out_cards={}
hole_cards=['2h','3c']
com_cards=['3s','4d', '5s','kh']

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
# returns set of all out-cards and their worth
def calculate_outs() -> dict:

    out_cards = {} # key = out card (string), value = rank of hand type the card is for (int)
    # examples of keys (for consistency): '3h','js','6d'

    # NOT NEEDED FOR TEST (passed in directly)
    # hole_cards = state.player_cards;
    # com_cards = state.community_cards;
    
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

    # store all seen ranks in dealt_ranks (eg [4, 11, 14, 4])
    dealt_ranks = []
    for card in dealt_cards:
        dealt_ranks.append(parse_card(card)[0])

    from collections import Counter
    # count each instance of seen ranks
    cnt = Counter(dealt_ranks) # example cnt = {4: 2, 11: 1, 14 : 1}
    num_pairs = 0
    num_trips = 0
    for rank_val, count in cnt.items():
        if count == 2: num_pairs+=1
        if count == 3: num_trips+=1


    # hand type functions:

    def four_of_a_kind() -> None:


        # in case rank is 10-13, make dict to convert letter represenation later
        face_card = {10 : 't', 11 : 'j', 12 : 'q', 13 : 'k', 14 : 'a'}

        for rank_val, count in cnt.items():
            if count == 3:
                for suit in "hdsc":
                    if (rank_val in face_card): # if face card, change its rank to the name (eg 11 -> 'J')
                        card_to_add = f"{face_card[rank_val]}{suit}"
                    else: # not a face card
                        card_to_add = f"{rank_val}{suit}"
                    if card_to_add not in dealt_cards:
                        add_out(card_to_add, 7)

    def full_house() -> None:

        # if there already exists two pairs
        if num_pairs == 2:
            # in case rank is 10-13, make dict to convert letter represenation later
            face_card = {10 : 't', 11 : 'j', 12 : 'q', 13 : 'k', 14 : 'a'}

            for rank_val, count in cnt.items():
                if count == 2:
                    for suit in "hdsc":
                        if (rank_val in face_card): # if face card, change its rank to the name (eg 11 -> 'J')
                            card_to_add = f"{face_card[rank_val]}{suit}"
                        else: # not a face card
                            card_to_add = f"{rank_val}{suit}"
                        if card_to_add not in dealt_cards:
                            add_out(card_to_add, 6)

        if num_trips >= 1 and num_pairs == 0:
            # in case rank is 10-13, make dict to convert letter represenation later
            face_card = {10 : 't', 11 : 'j', 12 : 'q', 13 : 'k', 14 : 'a'}

            for rank_val, count in cnt.items():
                if count == 1:
                    for suit in "hdsc":
                        if (rank_val in face_card): # if face card, change its rank to the name (eg 11 -> 'J')
                            card_to_add = f"{face_card[rank_val]}{suit}"
                        else: # not a face card
                            card_to_add = f"{rank_val}{suit}"
                        if card_to_add not in dealt_cards:
                            add_out(card_to_add, 6)

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
        # for converting rank format
        RANKS = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:'t', 11:'j', 12:'q', 13:'k', 14:'a'};

        # increment counter for every rank if it appears in dealt cards
        dealt_ranks = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0};
        for card in dealt_cards:
            dealt_ranks[parse_card(card)[0]]+=1;

        # check if the dealt ranks are 1 card away from a straight
        for r in dealt_ranks:
            if dealt_ranks[r]==0:
                # 2 [] 2  <--- means the outcard [] is the middle card in the straight
                if r > 3 and r < 13:
                    if (dealt_ranks[r-2]!=0 and dealt_ranks[r-1]!=0 and dealt_ranks[r+1]!=0 and dealt_ranks[r+2]!=0):
                        for suit in "hdsc":
                            add_out(f"{RANKS[r]}{suit}",4);
                            
                # 3 [] 1  <--- outcard [] is 4th card in the straight
                if r > 4 and r < 14:
                    if (dealt_ranks[r-3]!=0 and dealt_ranks[r-2]!=0 and dealt_ranks[r-1]!=0 and dealt_ranks[r+1]!=0):
                        for suit in "hdsc":
                            add_out(f"{RANKS[r]}{suit}",4);

                # 1 [] 3
                if r > 2 and r < 12:
                    if (dealt_ranks[r-1]!=0 and dealt_ranks[r+1]!=0 and dealt_ranks[r+2]!=0 and dealt_ranks[r+3]!=0):
                        for suit in "hdsc":
                            add_out(f"{RANKS[r]}{suit}",4);

                # 4 []
                if r > 5:
                    if (dealt_ranks[r-4]!=0 and dealt_ranks[r-3]!=0 and dealt_ranks[r-2]!=0 and dealt_ranks[r-1]!=0):
                        for suit in "hdsc":
                            add_out(f"{RANKS[r]}{suit}",4);

                # [] 4
                if r < 11:
                    if (dealt_ranks[r+1]!=0 and dealt_ranks[r+2]!=0 and dealt_ranks[r+3]!=0 and dealt_ranks[r+4]!=0):
                        for suit in "hdsc":
                            add_out(f"{RANKS[r]}{suit}",4);


        # special case: a2345

        dealt_a2345 = {14:0, 2:0, 3:0, 4:0, 5:0};
        dealt_a2345[14] = dealt_ranks[14]; # initalizing dict for a2345 case
        dealt_a2345[2] = dealt_ranks[2];
        dealt_a2345[3] = dealt_ranks[3];
        dealt_a2345[4] = dealt_ranks[4];
        dealt_a2345[5] = dealt_ranks[5];

        not_dealt = [];
        for r in dealt_a2345:
            if dealt_a2345[r]==0:
                not_dealt.append(r);
        if len(not_dealt)==1: # check if dealt cards are 1 card away from a2345 straight
            for suit in "hdsc":
                add_out(f"{RANKS[not_dealt[0]]}{suit}",4);



    def three_of_a_kind() -> None:

        # store all seen ranks in dealt_ranks (eg [4, 11, 14, 4])
        dealt_ranks = []
        for card in dealt_cards:
            dealt_ranks.append(parse_card(card)[0])

        # in case rank is 10-13, make dict to convert letter represenation later
        face_card = {10 : 't', 11 : 'j', 12 : 'q', 13 : 'k', 14 : 'a'}

        for rank_val, count in cnt.items():
            if count == 2:
                for suit in "hdsc":
                    if (rank_val in face_card): # if face card, change its rank to the name (eg 11 -> 'J')
                        card_to_add = f"{face_card[rank_val]}{suit}"
                    else: # not a face card
                        card_to_add = f"{rank_val}{suit}"
                    if card_to_add not in dealt_cards:
                        add_out(card_to_add, 3)


    def two_pair() -> None:

        # if there already exists one pair
        if num_pairs == 1:
            # in case rank is 10-13, make dict to convert letter represenation later
            face_card = {10 : 't', 11 : 'j', 12 : 'q', 13 : 'k', 14 : 'a'}

            for rank_val, count in cnt.items():
                if count == 1:
                    for suit in "hdsc":
                        if (rank_val in face_card): # if face card, change its rank to the name (eg 11 -> 'J')
                            card_to_add = f"{face_card[rank_val]}{suit}"
                        else: # not a face card
                            card_to_add = f"{rank_val}{suit}"
                        if card_to_add not in dealt_cards:
                            add_out(card_to_add, 2)

    def high_pair() -> None:
        # if already exists, pair, exit
        if num_pairs != 0:
            return

        
        from collections import Counter
        # count each instance of seen ranks
        cnt = Counter(dealt_ranks) # example cnt = {4: 2, 11: 1, 14 : 1}

        # in case rank is 10-13, make dict to convert letter represenation later
        face_card = {10 : 't', 11 : 'j', 12 : 'q', 13 : 'k', 14 : 'a'}

        for rank_val, count in cnt.items():
            if count == 1 and rank_val > 8:
                for suit in "hdsc":
                    if (rank_val in face_card): # if face card, change its rank to the name (eg 11 -> 'J')
                        card_to_add = f"{face_card[rank_val]}{suit}"
                    else: # not a face card
                        card_to_add = f"{rank_val}{suit}"
                    if card_to_add not in dealt_cards:
                        add_out(card_to_add, 1)

    def low_pair() -> None:
        # if already exists, pair, exit
        if num_pairs != 0:
            return

        # store all seen ranks in dealt_ranks (eg [4, 11, 14, 4])
        dealt_ranks = []
        for card in dealt_cards:
            dealt_ranks.append(parse_card(card)[0])


        # in case rank is 10-13, make dict to convert letter represenation later
        face_card = {10 : 't', 11 : 'j', 12 : 'q', 13 : 'k', 14 : 'a'}

        for rank_val, count in cnt.items():
            if count == 1 and rank_val <= 8:
                for suit in "hdsc":
                    if (rank_val in face_card): # if face card, change its rank to the name (eg 11 -> 'J')
                        card_to_add = f"{face_card[rank_val]}{suit}"
                    else: # not a face card
                        card_to_add = f"{rank_val}{suit}"
                    if card_to_add not in dealt_cards:
                        add_out(card_to_add, .5)


    # find all outs

    four_of_a_kind();
    full_house();
    flush();
    straight();
    three_of_a_kind();
    two_pair();
    high_pair();
    low_pair();

    return out_cards;
