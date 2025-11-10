

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

    # NOT INCLUDED FOR TEST (directly passed in)
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


    # hand type functions:

    def four_of_a_kind() -> None:

        # store all seen ranks in dealt_ranks (eg [4, 11, 14, 4])
        dealt_ranks = []
        for card in dealt_cards:
            dealt_ranks.append(parse_card(card)[0])

        
        from collections import Counter
        # count each instance of seen ranks
        cnt = Counter(dealt_ranks) # example cnt = {4: 2, 11: 1, 14 : 1}

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
                        add_out(card_to_add, 3)

    def full_house() -> None:
        pass

    def flush() -> None:
        pass

    def straight() -> None:
        pass

    def three_of_a_kind() -> None:

        # store all seen ranks in dealt_ranks (eg [4, 11, 14, 4])
        dealt_ranks = []
        for card in dealt_cards:
            dealt_ranks.append(parse_card(card)[0])

        
        from collections import Counter
        # count each instance of seen ranks
        cnt = Counter(dealt_ranks) # example cnt = {4: 2, 11: 1, 14 : 1}

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
        pass

    def high_pair() -> None:

        # store all seen ranks in dealt_ranks (eg [4, 11, 14, 4])
        dealt_ranks = []
        for card in dealt_cards:
            dealt_ranks.append(parse_card(card)[0])

        
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

        # store all seen ranks in dealt_ranks (eg [4, 11, 14, 4])
        dealt_ranks = []
        for card in dealt_cards:
            dealt_ranks.append(parse_card(card)[0])

        
        from collections import Counter
        # count each instance of seen ranks
        cnt = Counter(dealt_ranks) # example cnt = {4: 2, 11: 1, 14 : 1}

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
# ---------------- TEST HARNESS (paste below your code) ----------------

def run_test(hole, com):
    """
    hole, com: dict[str, int] - your globals (card -> any int)
    must_include: dict[str, int] - outs that MUST be present with exact worth
    must_not_include: set[str] - outs that MUST NOT appear
    """
    # use globals exactly like your code expects
    global hole_cards, com_cards
    hole_cards = hole.copy()
    com_cards  = com.copy()

    outs = calculate_outs()

    print(f"\n{name}")
    print("hole_cards:", hole_cards)
    print("com_cards :", com_cards)
    print("outs      :", outs)

    # basic sanity checks
    # 1) out keys should be 2-char lowercase like 'kh', '7c'
    for k in outs:
        assert isinstance(k, str) and len(k) == 2 and k == k.lower(), f"Out key not lowercase 2-char: {k}"

    # 2) outs must not include cards already dealt
    dealt = set(hole_cards) | set(com_cards)
    for k in outs:
        assert k not in dealt, f"Out contains already-dealt card: {k}"

    # 3) required outs
    if must_include:
        for k, v in must_include.items():
            assert k in outs, f"Missing required out: {k}"
            assert outs[k] == v, f"Wrong worth for {k}: got {outs[k]}, expected {v}"

    # 4) forbidden outs
    if must_not_include:
        for k in must_not_include:
            assert k not in outs, f"Unexpected out present: {k}"

    print("✓ Passed")

# ---------------- Example tests ----------------

# T1: Four-of-a-kind out from trips of kings (need 'kc'; worth should be 3 per your code)
run_test(
    "T1: Trips K → quad out",
    hole={"kd": 1, "jd": 1},
    com={"kh": 1, "ks": 1, "6d": 1},
    must_include={"kc": 3}
)

# T2: Already quads (no outs)
run_test(
    "T2: Already quads → no outs",
    hole={"7c": 1, "2d": 1},
    com={"7h": 1, "7d": 1, "7s": 1},
    must_not_include={"7h", "7d", "7s", "7c"}  # and generally outs should be empty
)

# T3: Three-of-a-kind outs from a pair of 9s (two missing suits)
# Pair = 9h, 9d; missing suits: 9s, 9c → both should be worth 3 (your three_of_a_kind uses 3)
run_test(
    "T3: Pair of 9s → trips outs",
    hole={"9h": 1, "2d": 1},
    com={"9d": 1, "qs": 1, "5c": 1},
    must_include={"9s": 3, "9c": 3}
)

# T4: High-pair outs from a single Ace (rank > 8) → propose remaining suits (worth 1)
# Only one Ace on table (ah). Expect ac, ad, as as outs with worth 1.
run_test(
    "T4: High pair from single Ace",
    hole={"ah": 1, "2c": 1},
    com={"kd": 1, "7s": 1, "4d": 1},
    must_include={"ac": 1, "ad": 1, "as": 1}
)

# T5: Low-pair outs from a single 5 (rank <= 8) → propose remaining suits (worth 0.5)
# Only one 5 on table (5h). Expect 5c, 5d, 5s as outs with worth 0.5.
run_test(
    "T5: Low pair from single 5",
    hole={"5h": 1, "tc": 1},
    com={"qd": 1, "7s": 1, "4d": 1},
    must_include={"5c": 0.5, "5d": 0.5, "5s": 0.5}
)

# T6: Face-rank mapping check for tens/jacks/queens/kings/aces (lowercase letters)
# Pair of tens → missing suits should be 'ts' and 'tc' (worth 3)
run_test(
    "T6: Face mapping for 't'",
    hole={"th": 1, "2d": 1},
    com={"td": 1, "9s": 1, "3c": 1},
    must_include={"ts": 3, "tc": 3}
)

# T7: No pairs/trips of any rank → three_of_a_kind/four_of_a_kind produce no outs
# (high_pair/low_pair will still add many proposals; here we *forbid* one that shouldn't appear)
run_test(
    "T7: No pairs or trips",
    hole={"ah": 1, "kd": 1},
    com={"9s": 1, "7c": 1, "3d": 1},
    must_not_include={"ac"} 
