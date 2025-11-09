out_cards={'3H':7,'JS':5,'6D':2} # key = out card (string), value = rank of hand type the card is for (int)
    
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

print(out_cards)
print("{'3H': 7, 'JS': 5, '6D': 2} expected \n")

add_out('9C', 1)
print(out_cards)
print("{'3H': 7, 'JS': 5, '6D': 2, '9C': 1} expected \n")

add_out('3H', 4)
print(out_cards)
print("{'3H': 7, 'JS': 5, '6D': 2, '9C': 1} expected \n")

add_out('6D', 4)
print(out_cards)
print("{'3H': 7, 'JS': 5, '6D': 4, '9C': 1} expected \n")

add_out('6D', 1)
print(out_cards)
print("{'3H': 7, 'JS': 5, '6D': 4, '9C': 1} expected \n")