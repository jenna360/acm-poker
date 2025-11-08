import sys, json
from types import SimpleNamespace
from bot import test

def to_obj(x):
    if isinstance(x, dict):
        return SimpleNamespace(**{k: to_obj(v) for k, v in x.items()})
    if isinstance(x, list):
        return [to_obj(v) for v in x]
    return x

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_test.py test.json")
        raise SystemExit(1)

    with open(sys.argv[1], "r") as f:
        state = json.load(f)          # dict
    state_obj = to_obj(state)         # -> object with .players, .pots[i].value, etc.

    test(state_obj)                   # pass object, not dict

if __name__ == "__main__":
    main()
