import keyboard as kb
import yaml
import random

with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

messages = data["messages"]
schizomsg = data["schizowords"]

seed_N = data["auto-complete-start"]
profanityinclude = data["profanity-include"]
schizopercent = data["schizophrenia%"]
drunkmode = data["drunkmode"]

keywords = ["fuck", "shit"]

NEIGHBORS = {
    "q": ["w", "a"],
    "w": ["q", "e", "a", "s"],
    "e": ["w", "r", "s", "d"],
    "r": ["e", "t", "d", "f"],
    "t": ["r", "y", "f", "g"],
    "y": ["t", "u", "g", "h"],
    "u": ["y", "i", "h", "j"],
    "i": ["u", "o", "j", "k"],
    "o": ["i", "p", "k", "l"],
    "p": ["o", "l"],
    "a": ["q", "w", "s", "z"],
    "s": ["a", "w", "e", "d", "z", "x"],
    "d": ["s", "e", "r", "f", "x", "c"],
    "f": ["d", "r", "t", "g", "c", "v"],
    "g": ["f", "t", "y", "h", "v", "b"],
    "h": ["g", "y", "u", "j", "b", "n"],
    "j": ["h", "u", "i", "k", "n", "m"],
    "k": ["j", "i", "o", "l", "m"],
    "l": ["k", "o", "p"],
    "z": ["a", "s", "x"],
    "x": ["z", "s", "d", "c"],
    "c": ["x", "d", "f", "v"],
    "v": ["c", "f", "g", "b"],
    "b": ["v", "g", "h", "n"],
    "n": ["b", "h", "j", "m"],
    "m": ["n", "j", "k"]
}

def get_neighbor_key(key: str) -> str:
    key = key.lower()
    return random.choice(NEIGHBORS.get(key, [key]))

sentence_cache = ""

print("good luck mortal")

while True:
    event = kb.read_event()
    if event.event_type != "down":
        continue

    key = event.name

    if key != "space" and (len(key) > 1):
        continue

    if random.randint(1, 100) <= schizopercent:
        kb.press_and_release("ctrl+a")
        kb.press_and_release("backspace")

        if random.randint(1, 2) == 1:
            kb.write(random.choice(schizomsg))
            kb.press_and_release("enter")
            sentence_cache = ""
            continue

        out = " " if key == "space" else key
        if len(out) == 1 and out.isalpha() and drunkmode:
            out = get_neighbor_key(out)

        kb.write(out)
        sentence_cache = ""
        continue

    key = " " if key == "space" else key

    if drunkmode and len(key) == 1 and key.isalpha():
        key = get_neighbor_key(key)

    sentence_cache += key

    sentence_candidate = []
    for sentence_item in messages:
        sentence_seed = " ".join(sentence_item.split(" ")[:seed_N])
        if sentence_seed.startswith(sentence_cache):
            sentence_candidate.append(sentence_item)

    if not sentence_candidate:
        continue

    sentence_candidate.sort(key=len, reverse=True)
    pick = random.choice(sentence_candidate)

    if not profanityinclude and any(k in pick.lower() for k in keywords):
        print("PROFANITY FOUND! RANDOM PICKING ANOTHER MESSAGE")
        pick2 = random.choice(sentence_candidate)
        print(f"Picked sentence: {pick2}")
        if not any(k in pick2.lower() for k in keywords):
            pick = pick2
        else:
            print("Hey... atleast we tried to pick again!")
            pick = pick2

    kb.write(pick[len(sentence_cache):])
    kb.press_and_release("enter")
    sentence_cache = ""
