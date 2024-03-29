from dataclasses import dataclass, field
from latindictinfl import *

def monospace(text: str):
    mapping = str.maketrans("0123456789", "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿")
    return text.translate(mapping)

def regularize(word: str) -> str:
    word = word.lower()
    mapping = str.maketrans("āēīōūȳjäëïöüÿáéíóúýàèìòùỳ",
                            "aeiouyiaeiouyaeiouyaeiouy")
    word = word.translate(mapping)
    word = word.replace('æ', "ae")
    word = word.replace('œ', "oe")
    word = word.replace('-', "")

    return word


@dataclass
class Definition(object):
    head: str
    tag: str | None = None
    construct: str | None = None
    note: str | None = None
    subdef: list["Definition"] = field(default_factory=lambda: [])

    def __eq__(self, __o) -> bool:
        if isinstance(__o, Definition):
            if self.head == __o.head and self.tag == __o.tag and self.construct == __o.construct:
                return True
        return False

class LatinEntry(object):

    def __init__(self,
                 head: str,
                 category: str,
                 inflect: str,
                 defs: list[Definition],
                 root: str | None = None,
                 note: str | None = None,
                 sr: str | None = None):
        self.head = head
        self.category = category
        self.inflect = inflect
        self.defs = defs
        self.root = root
        self.note = note
        self.sr = sr
        if not sr:
            if inflect == "-ī":
                self.sr = decl2(regularize(self.head))
            elif inflect == "-ae":
                self.sr = decl1(regularize(self.head))
            elif inflect == "-is" and head.endswith(("is", "es")):
                self.sr = decl3(regularize(self.head[:-2]), 'i')
            elif inflect == "-nis":
                self.sr = decl3(regularize(self.head + "n"))
            elif inflect == "-ōris":
                self.sr = decl3(regularize(self.head))
            elif inflect == "-tis" and head.endswith("tās"):
                self.sr = decl3(regularize(self.head[:-1] + 't'))
            elif inflect.startswith(("-entis", "-antis")):
                self.sr = decl3(regularize(self.head[:-1] + 't'), 'i')
            elif inflect == "-ūs":
                self.sr = decl4(regularize(self.head))
            elif inflect in ["-ēī", "-eī"]:
                self.sr = decl5(regularize(self.head))
            elif inflect == "-a/um":
                self.sr = adjDecl1(regularize(self.head))
            elif inflect == "-e":
                self.sr = adjDecl3(regularize(self.head[:-2]))
            elif inflect == "<1>":
                if head.endswith('ō'):
                    self.sr = conj1(regularize(self.head))
                elif head.endswith("or"):
                    self.sr = conj1d(regularize(self.head))

    def defListFormat(self, defs: list[Definition]):
        rs = []
        for i in range(len(defs)):
            d = defs[i]
            text = "{}.    {}{}{};{}".format(
                monospace(str(i + 1)), '(*' + d.tag + "*) " if d.tag else "",
                '(' + d.construct + ") " if d.construct else "", d.head,
                "\n    *" + d.note + '*' if d.note else "")
            rs.append(text)
        return '\n'.join(rs)

    def toText(self) -> str:
        text = "**{}**  *{}*{}{}\n{}{}"

        return text.format(self.head, self.category,
                           ", " + self.inflect if self.inflect else "",
                           "  [ __" + self.root + "__ ]" if self.root else "",
                           self.defListFormat(self.defs),
                           '\n> ' + self.note if self.note else "")

    def __eq__(self, __o) -> bool:
        if isinstance(__o, LatinEntry):
            if self.head == __o.head and self.category == __o.category and self.inflect == __o.inflect and self.defs == __o.defs:
                return True
        return False