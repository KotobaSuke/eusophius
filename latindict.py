from dataclasses import dataclass, field
from latindictbase import Definition, LatinEntry
from latindictinfl import *
from latindictsrc import dictEntries
import re
import random

def regularize(word: str) -> str:
        word = word.lower()
        mapping = str.maketrans("āēīōūȳjuäëïöüÿáéíóúýàèìòùỳ",
                                "aeiovyivaeiovyaeiovyaeiovy")
        word = word.translate(mapping)
        word = word.replace('æ', "ae")
        word = word.replace('œ', "oe")
        word = word.replace('-', "")
    
        return word

@dataclass
class LatinDict(object):
    entries: dict[tuple[str, int], LatinEntry]
    entryCount: int = 0

    def getInfo(self) -> str:
        return "Hoc est lexicon Latino-Anglicum a Kotobà Trilio factum.\nNunc insunt {} vocabula.".format(self.entryCount)

    def scan(self, filename):
        for e in dictEntries:
            try:
                self.addEntry(e.head, e)
                self.entryCount += 1
                if e.sr:
                    for s in e.sr:
                        self.addEntry(s, e)
            except BaseException as ex:
                print(ex, "with", e)
                continue

        self.entries = dict(sorted(self.entries.items(), key=lambda x: x[0]))

    def addEntry(self, entryName: str, entry: LatinEntry):
        entryName = regularize(entryName)
        i = 0
        while (entryName, i) in self.entries:
            i += 1
        self.entries[(entryName, i)] = entry

    def getEntry(self, entryName: str):
        entryName = regularize(entryName)
        i = 0
        entries = []
        while (entryName, i) in self.entries:
            isDuplicate = False
            for eIn in entries:
                if self.entries[(entryName, i)] == eIn:
                    isDuplicate = True
            if not isDuplicate:
                entries.append(self.entries[(entryName, i)])
            i += 1
        #print(entries, len(entries))
        return entries
    def getEntryByDef(self, query: str, precise: bool=False):
        entries = []
        for e in self.entries.values():
            isDuplicate = False
            for d in e.defs:
                if precise:
                    pattern = r"(\s|(^)){}[,;]".format(query)
                else:
                    pattern = r"\b{}\b".format(query)
                if re.search(pattern, d.head):
                    for eIn in entries:
                        if e == eIn:
                            isDuplicate = True
                    if not isDuplicate:
                        entries.append(e)
        return entries

    def getRandomEntry(self):
        entry = random.choice(list(self.entries.values()))
        return entry
    def getVolume(self) -> int:
        return self.entryCount


latinDict = LatinDict({})
