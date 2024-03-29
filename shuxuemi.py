import random
import pickle

with open("mi_model.pickle", "rb") as f:
    cfd: dict[str, dict] = pickle.load(f)

def generateModel(word: str) -> str:
    org = word
    text = ""
    for _ in range(1000):
        text += word
        for i in range(len(word)):
            if word[i:] in cfd:
                t = cfd[word[i:]]
                break
            if i == len(word) - 1:
                return "✗|" + word
        k, v = list(t.keys()), list(t.values())
        word = random.choices(k, weights=v)[0]
        if word == '\n':
            break
    if not text:
        return "*nihil*"
    if text == org:
        return "✗|" + text
    return "✓|" + text