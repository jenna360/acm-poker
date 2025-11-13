# <IMPORTS HERE>

# </IMPORTS HERE>

# <DO NOT MODIFY>
from helpers import *

class Pot:
    value: int
    players: list[str]


class GameState:
    index_to_action: int
    index_of_small_blind: int
    players: list[str]
    player_cards: list[str]
    held_money: list[int]
    bet_money: list[int]
    community_cards: list[str]
    pots: list[Pot]
    small_blind: int
    big_blind: int
# </DO NOT MODIFY>


""" Store any persistent data for your bot in this class """
class Memory:
    pass


""" Make a betting decision for the current turn.

    This function is called every time your bot needs to make a bet.

    Args:
        state (GameState): The current state of the game.
        memory (Memory | None): Your bot's memory from the previous turn, or None if this is the first turn.

    Returns:
        tuple[int, Memory | None]: A tuple containing:
            bet_amount: int - The amount you want to bet (-1 to fold, 0 to check, or any positive integer to raise)
            memory: Memory | None - Your bot's updated memory to be passed to the next turn
"""

def bet(state: GameState, memory: Memory | None=None) -> tuple[int, Memory | None]:
    bet_amount = bet_helper(state)
    return (bet_amount, memory)


# our functions:

# returns a fraction indicating position
# - smaller fraction means lower position (eg 1/7)
# - higher fraction means later position (eg 6/7)
def position(state: GameState) -> float:
    num_players = len(state.players)
    our_index = state.index_to_action
    small_blind = state.index_of_small_blind
    return ((our_index - small_blind) % num_players) / num_players


def pot_odds(state: GameState) -> float:
    pot_before_call = 0
    amt_to_call = amount_to_call(state);
    pots = get_my_pots(state);
    for pot in pots: # for each pot we're in, add the total of the pots
        pot_before_call += pot.value
    # print(f"Pot total {pot_before_call}")

    return amt_to_call / (pot_before_call + amt_to_call)

#def hand_equity(state: GameState) -> float:


# returns set of all out-cards and their worth
# to be used after flop and turn rounds only
def calculate_outs(state: GameState) -> dict:

    out_cards = {} # key = out card (string), value = rank of hand type the card is for (int)
    # examples of keys (for consistency): '3h','js','6d'

    hole_cards = state.player_cards;
    com_cards = state.community_cards;
    
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
                            add_out(card_to_add, 1)

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
                        add_out(card_to_add, .7)

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
                        add_out(card_to_add, .3)


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



def bet_helper(state: GameState, memory: Memory | None=None) -> tuple[int, Memory | None]:
    hand_strength = 20
    bet_amount = 0
    best_hand = get_best_hand_from(state.player_cards, state.community_cards)[0]
    # use best_hand (integer 0-8) in post-flop
    
    if get_round_name(state) == "Pre-Flop":
        card1_rank, card1_suit = parse_card(state.player_cards[0])
        card2_rank, card2_suit = parse_card(state.player_cards[1])

        # if we have a pocket pair
        if card1_rank == card2_rank:
            hand_strength += 2.2*card1_rank
        # if hole cards are suited and close together
        if card1_suit == card2_suit:
            hand_strength += max(card1_rank, card2_rank) - abs(card1_rank - card2_rank)
        # if hole cards are close in rank
        if 0 < abs(card1_rank - card2_rank) < 4:
            hand_strength += 3
        # if both hole cards are high (don't update for pockets)
        if card1_rank > 10 and card2_rank > 10 and (card1_rank != card2_rank):
            hand_strength += 10
        elif card1_rank > 6 and card2_rank > 6 and (card1_rank != card2_rank):
            hand_strength += 6
        # if early position
        if position(state) < .4:
            hand_strength -= 2
        # if late position
        if position(state) > .6:
            hand_strength += 5
        # if we're in dealer position
        if position(state) == 1:
            hand_strength += 7
        # if someone raised a lot
        if amount_to_call(state) > 3 * state.big_blind:
            hand_strength -= (amount_to_call(state)/state.big_blind) / 2.5 # this is kinda arbitrary lol

        # ---------------------------------
        # BETTING !!

        # very strong hand -> bet 5 times the big blind (or call, if that's larger)
        if hand_strength >= 60:
            bet_amount += max(6*state.big_blind, amount_to_call(state), min_raise(state))
        # moderately strong hand -> bet 4.5 times big blind
        elif 35 < hand_strength < 60:
            bet_amount += max(4.5*state.big_blind, amount_to_call(state), min_raise(state))
        # moderately strong hand -> bet 3 times big blind
        elif 25 < hand_strength < 35:
            bet_amount += max(3*state.big_blind, amount_to_call(state), min_raise(state))
        # mid hand -> fold to moderate raises
        elif 20 < hand_strength <= 25:
            if amount_to_call(state) > 4*state.big_blind:
                bet_amount = -1
            else:
                bet_amount = amount_to_call(state)
        # trash hand -> check or fold
        elif hand_strength <= 20:
            if amount_to_call(state) == 0:
                bet_amount = amount_to_call(state) # check
            else:
                bet_amount += -1 # fold

    elif get_round_name(state) == "Flop":
        outs_dict = calculate_outs(state)
        outs_strength = sum(outs_dict.values())
        hand_strength += outs_strength
        hand_strength += best_hand*4
            # can change multiplier, is arbitrary
            # (ex. if the bot's current best hand is a straight flush, this would add 8*5 = 40 to the hand strength)
            # (ex. if best hand is a pair, this would add 1*5 = 5 to the hand strength)

        if hand_strength >= 70:
            bet_amount = max(total_pot(state), amount_to_call(state), min_raise(state))
        # moderately strong hand -> bet 2.5 times big blind
        elif 40 < hand_strength < 70:
            bet_amount = max(.5*total_pot(state), amount_to_call(state), min_raise(state))
        # mid hand -> fold to moderate raises
        elif 30 < hand_strength <= 40:
            if amount_to_call(state) > .5*total_pot(state):
                bet_amount = -1
            else:
                bet_amount = amount_to_call(state)
        # trash hand -> check or fold
        elif hand_strength <= 30:
            if amount_to_call(state) <= .3*total_pot(state):
                bet_amount = amount_to_call(state) # check
            else:
                bet_amount = -1 # fold

    elif get_round_name(state) == "Turn":
        outs_dict = calculate_outs(state)
        outs_strength = (sum(outs_dict.values())) / 1.5
        hand_strength += outs_strength
        hand_strength += best_hand*4

        if hand_strength >= 70:
            bet_amount = max(total_pot(state), amount_to_call(state), min_raise(state))
        # moderately strong hand -> bet half pot
        elif 40 < hand_strength < 70:
            bet_amount = max(.5 * total_pot(state), min_raise(state))
        # mid hand -> fold to moderate raises
        elif 30 < hand_strength <= 40:
            if amount_to_call(state) > .5*total_pot(state):
                bet_amount = -1
            elif amount_to_call(state) == 0 and position(state) > .8: # if almost everyone checked -> senses weakness
                bet_amount = .7*total_pot(state)
            else:
                bet_amount = amount_to_call(state)
        # trash hand -> check or fold
        elif hand_strength <= 30:
            if amount_to_call(state) < (.3 * total_pot(state)):
                bet_amount = amount_to_call(state) # check
            else:
                bet_amount = -1 # fold

    elif get_round_name(state) == "River":
        hand_strength += best_hand*4 

        if hand_strength >= 50:
            bet_amount = max(total_pot(state), amount_to_call(state))
        # moderately strong hand -> bet 2.5 times big blind
        elif 40 < hand_strength < 50:
            bet_amount = 2*amount_to_call(state)
        # mid hand -> fold to moderate raises
        elif 30 < hand_strength <= 40:
            if amount_to_call(state) > .5*total_pot(state):
                bet_amount = -1
            else:
                bet_amount = amount_to_call(state)
        # trash hand -> check or fold
        elif hand_strength <= 30:
            if amount_to_call(state) < .2 * total_pot(state):
                bet_amount = amount_to_call(state) # check
            else:
                bet_amount = -1 # fold

    # check for invalid raises
    if min_raise(state) > bet_amount > amount_to_call(state):
        bet_amount = amount_to_call(state)
    if bet_amount > state.held_money[state.index_to_action]:
        bet_amount = state.held_money[state.index_to_action]
        
    # cast bet_amount back into an int
    return int(bet_amount)
