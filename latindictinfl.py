
def decl1(word: str, mode: str = None) -> list[str]:
    if word.endswith('a'):
        stem = word[:-1]
    else:
        raise ValueError(word)
    if not mode:
        endings = ["ae", "am", "arum", "is", "as"]
    elif mode == "bus":
        endings = ["ae", "am", "arum", "abus", "as"]
    else:
        raise ValueError(mode)
    return list(map(lambda x: stem + x, endings))


def decl2(word: str, mode: str = None) -> list[str]:
    if word.endswith("ius"):
        stem = word[:-2]
        if not mode:
            endings = ["i", "o", "um", "", "orum", "is", "os"]
        else:
            raise ValueError(mode)
    elif word.endswith("us"):
        stem = word[:-2]
        if not mode:
            endings = ["i", "o", "um", "e", "orum", "is", "os"]
        else:
            raise ValueError(mode)
    elif word.endswith("um"):
        stem = word[:-2]
        if not mode:
            endings = ["i", "o", "a", "orum", "is"]
        else:
            raise ValueError(mode)
    elif word.endswith("r"):
        if not mode:
            stem = word[:-2] + 'r'
            endings = ["i", "o", "um", "e", "orum", "is", "os"]
        elif mode == "er":
            stem = word
            endings = ["i", "o", "um", "e", "orum", "is", "os"]
        else:
            raise ValueError(mode)
    else:
        raise ValueError(word)

    return list(map(lambda x: stem + x, endings))


def decl3(stem: str, mode: str = None) -> list[str]:
    if not mode:
        endings = ["is", "i", "em", "e", "es", "um", "ibus"]
    elif mode == "n":
        endings = ["is", "i", "e", "a", "um", "ibus"]
    elif mode == "i":
        endings = ["is", "i", "em", "e", "es", "ium", "is", "ibus"]
    elif mode == "in":
        endings = ["is", "i", "e", "ia", "ium", "ibus"]

    return list(map(lambda x: stem + x, endings))


def decl4(word: str, mode: str = None) -> list[str]:
    if word.endswith("us"):
        stem = word[:-2]
        if not mode:
            endings = ["ui", "um", "u", "uum", "ibus"]
        else:
            raise ValueError(mode)
    elif word.endswith("u"):
        stem = word[:-1]
        if not mode:
            endings = ["us", "u", "ui", "ua", "uum", "ibus"]
        else:
            raise ValueError(mode)
    else:
        raise ValueError(word)

    return list(map(lambda x: stem + x, endings))


def decl5(word: str) -> list[str]:
    if word.endswith("es"):
        stem = word[:-2]
        endings = ["ei", "em", "e", "erum", "ebus"]
    else:
        raise ValueError(word)

    return list(map(lambda x: stem + x, endings))


def adjDecl1(word: str, mode: str = None, grade: bool = True) -> list[str]:
    if word.endswith("ius"):
        stem = word[:-2]
        if not mode:
            endings = ["i", "o", "um", "", "orum", "is", "os"]
        else:
            raise ValueError(mode)
    elif word.endswith("us"):
        stem = word[:-2]
        if not mode:
            endings = ["i", "o", "um", "e", "orum", "is", "os"]
        else:
            raise ValueError(mode)
    elif word.endswith("r"):
        if not mode:
            stem = word[:-2] + 'r'
            endings = ["i", "o", "um", "e", "orum", "is", "os"]
        elif mode == "er":
            stem = word
            endings = ["i", "o", "um", "e", "orum", "is", "os"]
        else:
            raise ValueError(mode)
    else:
        raise ValueError(word)
    endings += ["a", "ae", "am", "arum", "is", "as", "e"]
    if grade:
        endings += decl3("ior") + ["ior", "ius", "iora"]
        endings += list(
            set(
                decl1("issima") + decl2("issimus") + decl2("issimum") +
                ["issime"]))

    return list(map(lambda x: stem + x, endings))


def adjDecl3(stem: str, mode: str = "i", grade: bool = True) -> list[str]:
    endings = decl3("", mode) + ["iter"]
    if grade:
        endings += decl3("ior") + ["ior", "ius", "iora"]
        endings += list(
            set(
                decl1("issima") + decl2("issimus") + decl2("issimum") +
                ["issime"]))

    return list(map(lambda x: stem + x, endings))


def conj1(word: str, perfStem: str = "", gerundStem: str = "") -> list[str]:
    if word.endswith("o"):
        stem = word[:-1]
    else:
        raise ValueError(word)

    if perfStem == "": perfStem = stem + "av"
    if gerundStem == "": gerundStem = stem + "at"

    mainEndings = [
        "as", "at", "amus", "atis", "ant", "abam", "abas", "abat", "abamus",
        "abatis", "abant", "abo", "abis", "abit", "abimus", "abitis", "abunt",
        "or", "aris", "atur", "amur", "amini", "antur", "abar", "abaris",
        "abatur", "abamur", "abamini", "abantur", "abor", "aberis", "abitur",
        "abimur", "abimini", "abuntur", "em", "es", "et", "emus", "etis",
        "ent", "arem", "ares", "aret", "aremus", "aretis", "arent", "er",
        "eris", "etur", "emur", "emini", "entur", "arer", "areris", "aretur",
        "aremur", "aremini", "arentur", "a", "ate", "ato", "atote", "are",
        "andi", "ando", "andum", "ari"
    ]
    perfEndings = [
        "i", "isti", "it", "imus", "istis", "erunt", "ere", "eram", "eras",
        "erat", "eramus", "eratis", "erant", "ero", "eris", "erit", "erimus",
        "eritis", "erint", "erim", "issem", "isses", "issemus", "issetis",
        "issent", "isse"
    ]
    presPtcps = [stem + "ans"] + adjDecl3(stem + "ant", 'i')
    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        perfPtcps, futrPtcps = [], []
    gerundives = [stem + "andus"] + adjDecl1(stem + "andus")

    return list(
        set(
            list(map(lambda x: stem + x, mainEndings)) +
            list(map(lambda x: perfStem + x, perfEndings)) + presPtcps +
            perfPtcps + futrPtcps + gerundives))


def conj1d(word: str, gerundStem: str = "") -> list[str]:
    if word.endswith("or"):
        stem = word[:-2]
    else:
        raise ValueError(word)

    if gerundStem == "": gerundStem = stem + "at"

    mainEndings = [
        "or", "aris", "atur", "amur", "amini", "antur", "abar", "abaris",
        "abatur", "abamur", "abamini", "abantur", "abor", "aberis", "abitur",
        "abimur", "abimini", "abuntur", "er", "eris", "etur", "emur", "emini",
        "entur", "arer", "areris", "aretur", "aremur", "aremini", "arentur",
        "are", "andi", "ando", "andum", "ari"
    ]
    presPtcps = [stem + "ans"] + adjDecl3(stem + "ant", 'i')
    perfPtcps = [gerundStem + "us", gerundStem + "u"
                 ] + adjDecl1(gerundStem + "us")
    futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    gerundives = [stem + "andus"] + adjDecl1(stem + "andus")

    return list(
        set(
            list(map(lambda x: stem + x, mainEndings)) + presPtcps +
            perfPtcps + futrPtcps + gerundives))


def conj2(word: str, perfStem: str, gerundStem: str) -> list[str]:
    if word.endswith("eo"):
        stem = word[:-2]
    else:
        raise ValueError(word)

    mainEndings = [
        "es", "et", "emus", "etis", "ent", "ebam", "ebas", "ebat", "ebamus",
        "ebatis", "ebant", "ebo", "ebis", "ebit", "ebimus", "ebitis", "ebunt",
        "eor", "eris", "etur", "emur", "emini", "entur", "ebar", "ebaris",
        "ebatur", "ebamur", "ebamini", "ebantur", "ebor", "eberis", "ebitur",
        "ebimur", "ebimini", "ebuntur", "eam", "eas", "eat", "eamus", "eatis",
        "eant", "erem", "eres", "eret", "eremus", "eretis", "erent", "ear",
        "earis", "eatur", "eamur", "eamini", "eantur", "erer", "ereris",
        "eretur", "eremur", "eremini", "erentur", "e", "ete", "eto", "etote",
        "ere", "endi", "endo", "endum", "eri"
    ]
    perfEndings = [
        "i", "isti", "it", "imus", "istis", "erunt", "ere", "eram", "eras",
        "erat", "eramus", "eratis", "erant", "ero", "eris", "erit", "erimus",
        "eritis", "erint", "erim", "issem", "isses", "issemus", "issetis",
        "issent", "isse"
    ]
    presPtcps = [stem + "ens"] + adjDecl3(stem + "ent", 'i')
    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        perfPtcps = []
        futrPtcps = []
    gerundives = [stem + "endus"] + adjDecl1(stem + "endus")
    if perfStem:
        return list(
            set(
                list(map(lambda x: stem + x, mainEndings)) +
                list(map(lambda x: perfStem + x, perfEndings)) + presPtcps +
                perfPtcps + futrPtcps + gerundives))
    else:
        return list(
            set(
                list(map(lambda x: stem + x, mainEndings)) + presPtcps +
                perfPtcps + futrPtcps + gerundives))


def conj2d(word: str, gerundStem: str) -> list[str]:
    if word.endswith("eor"):
        stem = word[:-3]
    else:
        raise ValueError(word)

    mainEndings = [
        "eor", "eris", "etur", "emur", "emini", "entur", "ebar", "ebaris",
        "ebatur", "ebamur", "ebamini", "ebantur", "ebor", "eberis", "ebitur",
        "ebimur", "ebimini", "ebuntur", "ear", "earis", "eatur", "eamur",
        "eamini", "eantur", "erer", "ereris", "eretur", "eremur", "eremini",
        "erentur", "ere", "endi", "endo", "endum", "eri"
    ]
    presPtcps = [stem + "ens"] + adjDecl3(stem + "ent", 'i')
    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        futrPtcps = []
    gerundives = [stem + "endus"] + adjDecl1(stem + "endus")
    return list(
        set(
            list(map(lambda x: stem + x, mainEndings)) + presPtcps +
            perfPtcps + futrPtcps + gerundives))


def conj2sd(word: str, gerundStem: str) -> list[str]:
    if word.endswith("eo"):
        stem = word[:-2]
    else:
        raise ValueError(word)

    mainEndings = [
        "es", "et", "emus", "etis", "ent", "ebam", "ebas", "ebat", "ebamus",
        "ebatis", "ebant", "ebo", "ebis", "ebit", "ebimus", "ebitis", "ebunt",
        "eam", "eas", "eat", "eamus", "eatis", "eant", "erem", "eres", "eret",
        "eremus", "eretis", "erent", "e", "ete", "eto", "etote", "ere", "endi",
        "endo", "endum", "eri"
    ]
    presPtcps = [stem + "ens"] + adjDecl3(stem + "ent", 'i')
    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        perfPtcps = []
        futrPtcps = []
    return list(
        set(
            list(map(lambda x: stem + x, mainEndings)) + presPtcps +
            perfPtcps + futrPtcps))


def conj3(word: str, perfStem: str, gerundStem: str, mode: str="") -> list[str]:
    if word.endswith("io"):
        stem = word[:-2]
        mode = "i"
    elif word.endswith("o"):
        stem = word[:-1]
    else:
        raise ValueError(word)

    if not mode:
        mainEndings = [
            "is", "it", "imus", "itis", "iunt", "ebam", "ebas", "ebat",
            "ebamus", "ebatis", "ebant", "am", "es", "et", "emus", "etis",
            "ent", "or", "eris", "itur", "imur", "imini", "untur", "ebar",
            "ebaris", "ebatur", "ebamur", "ebamini", "ebantur", "ar", "etur",
            "emur", "emini", "entur", "am", "as", "at", "amus", "atis", "ant",
            "erem", "eres", "eret", "eremus", "eretis", "erent", "aris",
            "atur", "amur", "amini", "antur", "erer", "ereris", "eretur",
            "eremur", "eremini", "erentur", "e", "ite", "ito", "itote", "ere",
            "endi", "endo", "endum", "i"
        ]
        presPtcps = [stem + "ens"] + adjDecl3(stem + "ent", 'i')
        gerundives = [stem + "endus"] + adjDecl1(stem + "endus")
    elif mode == "i":
        mainEndings = [
            "is", "it", "imus", "itis", "iunt", "iebam", "iebas", "iebat",
            "iebamus", "iebatis", "iebant", "iam", "ies", "iet", "iemus",
            "ietis", "ient", "ior", "ieris", "itur", "imur", "imini", "iuntur",
            "iebar", "iebaris", "iebatur", "iebamur", "iebamini", "iebantur",
            "iar", "ietur", "iemur", "iemini", "ientur", "iam", "ias", "iat",
            "iamus", "iatis", "iant", "erem", "eres", "eret", "eremus",
            "eretis", "erent", "iaris", "iatur", "iamur", "iamini",
            "iantur", "erer", "ereris", "eretur", "eremur", "eremini",
            "erentur", "e", "ite", "ito", "itote", "ere", "iendi", "iendo",
            "iendum", "i"
        ]
        presPtcps = [stem + "iens"] + adjDecl3(stem + "ient", 'i')
        gerundives = [stem + "iendus"] + adjDecl1(stem + "iendus")
    perfEndings = [
        "i", "isti", "it", "imus", "istis", "erunt", "ere", "eram", "eras",
        "erat", "eramus", "eratis", "erant", "ero", "eris", "erit", "erimus",
        "eritis", "erint", "erim", "issem", "isses", "issemus", "issetis",
        "issent", "isse"
    ]
    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        perfPtcps = []
        futrPtcps = []

    if perfStem:
        return list(set(
            list(map(lambda x: stem + x, mainEndings)) +
            list(map(lambda x: perfStem + x, perfEndings)) + presPtcps +
            perfPtcps + futrPtcps + gerundives))
    else:
        return list(set(
            list(map(lambda x: stem + x, mainEndings)) +
            presPtcps + perfPtcps + futrPtcps + gerundives))


def conj3d(word: str, gerundStem: str, mode: str="") -> list[str]:
    if word.endswith("ior"):
        stem = word[:-3]
        mode = "i"
    elif word.endswith("or"):
        stem = word[:-2]
    else:
        raise ValueError(word)

    if not mode:
        mainEndings = [
            "or", "eris", "itur", "imur", "imini", "untur", "ebar", "ebaris",
            "ebatur", "ebamur", "ebamini", "ebantur", "ar", "etur", "emur",
            "emini", "entur", "aris", "atur", "amur", "amini", "antur",
            "erer", "ereris", "eretur", "eremur", "eremini", "erentur", "ere",
            "endi", "endo", "endum", "i"
        ]
        presPtcps = [stem + "ens"] + adjDecl3(stem + "ent", 'i')
        gerundives = [stem + "endus"] + adjDecl1(stem + "endus")
    elif mode == "i":
        mainEndings = [
            "ior", "ieris", "itur", "imur", "imini", "iuntur",
            "iebar", "iebaris", "iebatur", "iebamur", "iebamini", "iebantur",
            "iar", "ietur", "iemur", "iemini", "ientur",
            "iaris", "iatur", "iamur", "iamini",
            "iantur", "erer", "ereris", "eretur", "eremur", "eremini",
            "erentur", "ere", "iendi", "iendo",
            "iendum", "i"
        ]
        presPtcps = [stem + "iens"] + adjDecl3(stem + "ient", 'i')
        gerundives = [stem + "iendus"] + adjDecl1(stem + "iendus")

    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        perfPtcps = []
        futrPtcps = []

    return list(
        set(
            list(map(lambda x: stem + x, mainEndings)) + presPtcps +
            perfPtcps + futrPtcps + gerundives))

def conj3sd(word: str, gerundStem: str, mode: str="") -> list[str]:
    if word.endswith("o"):
        stem = word[:-1]
    else:
        raise ValueError(word)

    mainEndings = [
        "or", "eris", "itur", "imur", "imini", "untur", "ebar", "ebaris",
        "ebatur", "ebamur", "ebamini", "ebantur", "ar", "etur", "emur",
        "emini", "entur", "aris", "atur", "amur", "amini", "antur",
        "erer", "ereris", "eretur", "eremur", "eremini", "erentur", "ere",
        "endi", "endo", "endum", "i"
    ]
    presPtcps = [stem + "ens"] + adjDecl3(stem + "ent", 'i')
    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        perfPtcps = []
        futrPtcps = []
    return list(
        set(
            list(map(lambda x: stem + x, mainEndings)) + presPtcps +
            perfPtcps + futrPtcps))

def conj4(word: str, perfStem: str, gerundStem: str) -> list[str]:
    if word.endswith("io"):
        stem = word[:-2]
    else:
        raise ValueError(word)

    mainEndings = [
        "is", "it", "imus", "itis", "iunt", "iebam", "iebas", "iebat",
        "iebamus", "iebatis", "iebant", "iam", "ies", "iet", "iemus", "ietis",
        "ient", "ior", "iris", "itur", "imur", "imini", "iuntur", "iebar",
        "iebaris", "iebatur", "iebamur", "iebamini", "iebantur", "iar",
        "ieris", "ietur", "iemur", "iemini", "ientur", "iam", "ias", "iat",
        "iamus", "iatis", "iant", "irem", "ires", "iret", "iremus", "iretis",
        "irent", "iar", "iaris", "iatur", "iamur", "iamini", "iantur", "irer",
        "ireris", "iretur", "iremur", "iremini", "irentur", "i", "ite", "ito",
        "itote", "ire", "iendi", "iendo", "iendum", "i"
    ]
    perfEndings = [
        "i", "isti", "it", "imus", "istis", "erunt", "ere", "eram", "eras",
        "erat", "eramus", "eratis", "erant", "ero", "eris", "erit", "erimus",
        "eritis", "erint", "erim", "issem", "isses", "issemus", "issetis",
        "issent", "isse"
    ]
    presPtcps = [stem + "iens"] + adjDecl3(stem + "ient", 'i')
    gerundives = [stem + "iendus"] + adjDecl1(stem + "iendus")
    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        perfPtcps = []
        futrPtcps = []

    if perfStem:
        return list(set(
            list(map(lambda x: stem + x, mainEndings)) +
            list(map(lambda x: perfStem + x, perfEndings)) + presPtcps +
            perfPtcps + futrPtcps + gerundives))
    else:
        return list(set(
            list(map(lambda x: stem + x, mainEndings)) +
            presPtcps + perfPtcps + futrPtcps + gerundives))


def conj4d(word: str, gerundStem: str) -> list[str]:
    if word.endswith("ior"):
        stem = word[:-3]
    else:
        raise ValueError(word)

    mainEndings = [
        "ior", "iris", "itur", "imur", "imini", "iuntur", "iebar", "iebaris",
        "iebatur", "iebamur", "iebamini", "iebantur", "iar", "ieris", "ietur",
        "iemur", "iemini", "ientur", "iar", "iaris", "iatur", "iamur",
        "iamini", "iantur", "irer", "ireris", "iretur", "iremur", "iremini",
        "irentur", "ire", "iendi", "iendo", "iendum", "i"
    ]
    presPtcps = [stem + "iens"] + adjDecl3(stem + "ient", 'i')
    gerundives = [stem + "iendus"] + adjDecl1(stem + "iendus")
    if gerundStem:
        perfPtcps = [gerundStem + "us", gerundStem + "u"
                     ] + adjDecl1(gerundStem + "us")
        futrPtcps = [gerundStem + "urus"] + adjDecl1(gerundStem + "urus")
    else:
        perfPtcps = []
        futrPtcps = []

    return list(
        set(
            list(map(lambda x: stem + x, mainEndings)) + presPtcps +
            perfPtcps + futrPtcps + gerundives))


IRR_INFL = {
    "sum": [
        "es", "est", "sumus", "estis", "sunt", "eram", "eras", "erat",
        "eramus", "eratis", "erant", "ero", "eris", "ere", "erit", "erimus",
        "eritis", "erunt", "fui", "fuisti", "fuit", "fuimus", "fuistis",
        "fuerunt", "fuere", "fueram", "fueras", "fuerat", "fueramus",
        "fueratis", "fuerant", "fuero", "fueris", "fuerit", "fuerimus",
        "fueritis", "fuerint", "sim", "sis", "sit", "simus", "sitis", "sint",
        "essem", "esses", "esset", "essemus", "essetis", "essent", "forem",
        "fores", "foret", "foremus", "foretis", "forent", "fuerim", "fuissem",
        "fuisses", "fuisset", "fuissemus", "fuissetis", "fuissent", "este",
        "esto", "estote", "fore", "esse", "fuisse", "futurus", "fore"
    ] + adjDecl1("futurus"),
    "absum": [
        "abes", "abest", "absumus", "abestis", "absunt", "aberam", "aberas",
        "aberat", "aberamus", "aberatis", "aberant", "abero", "aberis",
        "abere", "aberit", "aberimus", "aberitis", "aberunt", "afui",
        "afuisti", "afuit", "afuimus", "afuistis", "afuerunt", "afuere",
        "afueram", "afueras", "afuerat", "afueramus", "afueratis", "afuerant",
        "afuero", "afueris", "afuerit", "afuerimus", "afueritis", "afuerint",
        "absim", "absis", "absit", "absimus", "absitis", "absint", "abessem",
        "abesses", "abesset", "abessemus", "abessetis", "abessent", "aforem",
        "afores", "aforet", "aforemus", "aforetis", "aforent", "afuerim",
        "afuissem", "afuisses", "afuisset", "afuissemus", "afuissetis",
        "afuissent", "abeste", "abesto", "abestote", "afore", "abesse",
        "afuisse", "afuturus", "afore", "absens"
    ] + adjDecl1("afuturus") + adjDecl3("absent"),
    "adsum": [
        "ades", "adest", "adsumus", "adestis", "adsunt", "aderam", "aderas",
        "aderat", "aderamus", "aderatis", "aderant", "adero", "aderis",
        "adere", "aderit", "aderimus", "aderitis", "aderunt", "adfui",
        "adfuisti", "adfuit", "adfuimus", "adfuistis", "adfuerunt", "adfuere",
        "adfueram", "adfueras", "adfuerat", "adfueramus", "adfueratis",
        "adfuerant", "adfuero", "adfueris", "adfuerit", "adfuerimus",
        "adfueritis", "adfuerint", "adsim", "adsis", "adsit", "adsimus",
        "adsitis", "adsint", "adessem", "adesses", "adesset", "adessemus",
        "adessetis", "adessent", "adforem", "adfores", "adforet", "adforemus",
        "adforetis", "adforent", "adfuerim", "adfuissem", "adfuisses",
        "adfuisset", "adfuissemus", "adfuissetis", "adfuissent", "adeste",
        "adesto", "adestote", "adfore", "adesse", "adfuisse", "adfuturus",
        "adfore"
    ] + adjDecl1("adfuturus"),
    "insum": [
        "ines", "inest", "insumus", "inestis", "insunt", "ineram", "ineras",
        "inerat", "ineramus", "ineratis", "inerant", "inero", "ineris",
        "inere", "inerit", "inerimus", "ineritis", "inerunt", "infui",
        "infuisti", "infuit", "infuimus", "infuistis", "infuerunt", "infuere",
        "infueram", "infueras", "infuerat", "infueramus", "infueratis",
        "infuerant", "infuero", "infueris", "infuerit", "infuerimus",
        "infueritis", "infuerint", "insim", "insis", "insit", "insimus",
        "insitis", "insint", "inessem", "inesses", "inesset", "inessemus",
        "inessetis", "inessent", "inforem", "infores", "inforet", "inforemus",
        "inforetis", "inforent", "infuerim", "infuissem", "infuisses",
        "infuisset", "infuissemus", "infuissetis", "infuissent", "ineste",
        "inesto", "inestote", "infore", "inesse", "infuisse", "infuturus",
        "infore"
    ] + adjDecl1("infuturus"),
    "prosum": [
        "prodes", "prodest", "prosumus", "prodestis", "prosunt", "proderam", "proderas",
        "proderat", "proderamus", "proderatis", "proderant", "prodero", "proderis",
        "prodere", "proderit", "proderimus", "proderitis", "proderunt", "profui",
        "profuisti", "profuit", "profuimus", "profuistis", "profuerunt", "profuere",
        "profueram", "profueras", "profuerat", "profueramus", "profueratis",
        "profuerant", "profuero", "profueris", "profuerit", "profuerimus",
        "profueritis", "profuerprot", "prosim", "prosis", "prosit", "prosimus",
        "prositis", "prosprot", "prodessem", "prodesses", "prodesset", "prodessemus",
        "prodessetis", "prodessent", "proforem", "profores", "proforet", "proforemus",
        "proforetis", "proforent", "profuerim", "profuissem", "profuisses",
        "profuisset", "profuissemus", "profuissetis", "profuissent", "prodeste",
        "prodesto", "prodestote", "profore", "prodesse", "profuisse", "profuturus",
        "profore"
    ] + adjDecl1("profuturus"),
    "possum": [
        "potes", "potest", "possumus", "potestis", "possunt", "poteram",
        "poteras", "poterat", "poteramus", "poteratis", "poterant", "potero",
        "poteris", "potere", "poterit", "poterimus", "poteritis", "poterunt",
        "potui", "potuisti", "potuit", "potuimus", "potuistis", "potuerunt",
        "potuere", "potueram", "potueras", "potuerat", "potueramus",
        "potueratis", "potuerant", "potuero", "potueris", "potuerit",
        "potuerimus", "potueritis", "potuerint", "possim", "possis", "possit",
        "possimus", "possitis", "possint", "potessem", "potesses", "potesset",
        "potessemus", "potessetis", "potessent", "potuerim", "potuissem",
        "potuisses", "potuisset", "potuissemus", "potuissetis", "potuissent",
        "poteste", "potesse", "potuisse", "potuturus", "potens"
    ] + adjDecl3("potent"),
    "volo": [
        "volō", "vīs", "vult", "volt", "volumus", "vultis", "voltis", "volunt",
        "volēbam", "volēbās", "volēbat", "volēbāmus", "volēbātis", "volēbant",
        "volam", "volēs", "volet", "volēmus", "volētis", "volent", "voluī",
        "voluistī", "voluit", "voluimus", "voluistis", "voluērunt", "voluēre",
        "volueram", "voluerās", "voluerat", "voluerāmus", "voluerātis",
        "voluerant", "voluerō", "volueris", "voluerit", "voluerimus",
        "volueritis", "voluerint", "velim", "velīs", "velit", "velīmus",
        "velītis", "velint", "vellem", "vellēs", "vellet", "vellēmus",
        "vellētis", "vellent", "voluerim", "voluerīs", "voluerit",
        "voluerīmus", "voluerītis", "voluerint", "voluissem", "voluissēs",
        "voluisset", "voluissēmus", "voluissētis", "voluissent", "velle",
        "voluisse", "volēns"
    ] + adjDecl3("volent"),
    "malo": [
        "malō", "vīs", "vult", "malt", "malumus", "vultis", "maltis", "malunt",
        "malēbam", "malēbās", "malēbat", "malēbāmus", "malēbātis", "malēbant",
        "malam", "malēs", "malet", "malēmus", "malētis", "malent", "maluī",
        "maluistī", "maluit", "maluimus", "maluistis", "maluērunt", "maluēre",
        "malueram", "maluerās", "maluerat", "maluerāmus", "maluerātis",
        "maluerant", "maluerō", "malueris", "maluerit", "maluerimus",
        "malueritis", "maluerint", "malim", "malīs", "malit", "malīmus",
        "malītis", "malint", "mallem", "mallēs", "mallet", "mallēmus",
        "mallētis", "mallent", "maluerim", "maluerīs", "maluerit",
        "maluerīmus", "maluerītis", "maluerint", "maluissem", "maluissēs",
        "maluisset", "maluissēmus", "maluissētis", "maluissent", "malle",
        "maluisse", "malēns"
    ] + adjDecl3("malent"),
    "eo": [
        "eō", "īs", "it", "īmus", "ītis", "eunt", "ībam", "ībās", "ībat",
        "ībāmus", "ībātis", "ībant", "ībō", "ībis", "ībit", "ībimus", "ībitis",
        "ībunt", "iī", "īvī", "īstī", "īvistī", "iit", "īvit", "iimus",
        "īstis", "iērunt", "iēre", "ieram", "ierās", "ierat", "ierāmus",
        "ierātis", "ierant", "perfect", "ierō", "ieris", "ierit", "ierimus",
        "ieritis", "ierint", "eor", "īris", "īre", "ītur", "īmur", "īminī",
        "euntur", "ībar", "ībāris", "ībāre", "ībātur", "ībāmur", "ībāminī",
        "ībantur", "ībor", "īberis", "ībere", "ībitur", "ībimur", "ībiminī",
        "ībuntur", "eam", "eās", "eat", "eāmus", "eātis", "eant", "īrem",
        "īrēs", "īret", "īrēmus", "īrētis", "īrent", "ierim", "ierīs", "ierit",
        "ierīmus", "ierītis", "ierint", "īssem", "īssēs", "īsset", "īssēmus",
        "īssētis", "īssent", "ear", "eāris", "eāre", "eātur", "eāmur",
        "eāminī", "eantur", "īrer", "īrēris", "īrēre", "īrētur", "īrēmur",
        "īrēminī", "īrentur", "ī", "īte", "ītō", "ītōte", "euntō", "īre",
        "īminī", "ītor", "euntor", "īsse", "īrī", "iēns", "itūrus", "itus",
        "eundus", "eundī", "eundō", "eundum", "eundō", "itū"
    ] + adjDecl1("itus") + adjDecl1("iturus") + adjDecl3("ient"),
    "inquam": [
        "inquis", "inquit", "inquimus", "inquitis", "inquiunt", "inquiebat",
        "inquies", "inquiet", "inquii", "inquisti", "inquiat", "inque",
        "inquito", "inquiens"
    ],
    "fero": [
        "ferō", "fers", "fert", "ferimus", "fertis", "ferunt", "ferēbam",
        "ferēbās", "ferēbat", "ferēbāmus", "ferēbātis", "ferēbant", "feram",
        "ferēs", "feret", "ferēmus", "ferētis", "ferent", "tulī", "tulistī",
        "tulit", "tulimus", "tulistis", "tulērunt", "tulēre", "tetulērunt",
        "tuleram", "tulerās", "tulerat", "tulerāmus", "tulerātis", "tulerant",
        "tulerō", "tuleris", "tulerit", "tulerimus", "tuleritis",
        "tulerint", "feror", "ferris", "ferre", "fertur", "ferimur",
        "feriminī", "feruntur", "ferēbar", "ferēbāris", "ferēbāre",
        "ferēbātur", "ferēbāmur", "ferēbāminī", "ferēbantur", "ferar",
        "ferēris", "ferēre", "ferētur", "ferēmur", "ferēminī", "ferentur",
        "feram", "ferās", "ferat", "ferāmus", "ferātis", "ferant", "ferrem",
        "ferrēs", "ferret", "ferrēmus", "ferrētis", "ferrent", "tulerim",
        "tulerīs", "tulerit", "tulerīmus", "tulerītis", "tulerint", "",
        "tulissem", "tulissēs", "tulisset", "tulissēmus", "tulissētis",
        "tulissent", "", "ferar", "ferāris", "ferāre", "ferātur", "ferāmur",
        "ferāminī", "ferantur", "ferrer", "ferrēris", "ferrēre", "ferrētur",
        "ferrēmur", "ferrēminī", "ferrentur", "fer", "ferte", "fertō",
        "fertōte", "feruntō", "ferre", "feriminī", "fertor", "feruntor",
        "ferendī", "ferendō", "ferendum", "ferendō", "lātum", "lātū"
    ] + adjDecl3("ferent"),
    "aufero": [
        "auferō", "aufers", "aufert", "auferimus", "aufertis", "auferunt", "auferēbam",
        "auferēbās", "auferēbat", "auferēbāmus", "auferēbātis", "auferēbant", "auferam",
        "auferēs", "auferet", "auferēmus", "auferētis", "auferent", "abstulī", "abstulistī",
        "abstulit", "abstulimus", "abstulistis", "abstulērunt", "abstulēre", "abstetulērunt",
        "abstuleram", "abstulerās", "abstulerat", "abstulerāmus", "abstulerātis", "abstulerant",
        "abstulerō", "abstuleris", "abstulerit", "abstulerimus", "abstuleritis",
        "abstulerint", "auferor", "auferris", "auferre", "aufertur", "auferimur",
        "auferiminī", "auferuntur", "auferēbar", "auferēbāris", "auferēbāre",
        "auferēbātur", "auferēbāmur", "auferēbāminī", "auferēbantur", "auferar",
        "auferēris", "auferēre", "auferētur", "auferēmur", "auferēminī", "auferentur",
        "auferam", "auferās", "auferat", "auferāmus", "auferātis", "auferant", "auferrem",
        "auferrēs", "auferret", "auferrēmus", "auferrētis", "auferrent", "abstulerim",
        "abstulerīs", "abstulerit", "abstulerīmus", "abstulerītis", "abstulerint", "",
        "abstulissem", "abstulissēs", "abstulisset", "abstulissēmus", "abstulissētis",
        "abstulissent", "", "auferar", "auferāris", "auferāre", "auferātur", "auferāmur",
        "auferāminī", "auferantur", "auferrer", "auferrēris", "auferrēre", "auferrētur",
        "auferrēmur", "auferrēminī", "auferrentur", "aufer", "auferte", "aufertō",
        "aufertōte", "auferuntō", "auferre", "auferiminī", "aufertor", "auferuntor",
        "auferendī", "auferendō", "auferendum", "auferendō", "ablātum", "ablātū"
    ] + adjDecl3("auferent"),
    "offero": [
        "offerō", "offers", "offert", "offerimus", "offertis", "offerunt", "offerēbam",
        "offerēbās", "offerēbat", "offerēbāmus", "offerēbātis", "offerēbant", "offeram",
        "offerēs", "offeret", "offerēmus", "offerētis", "offerent", "obtulī", "obtulistī",
        "obtulit", "obtulimus", "obtulistis", "obtulērunt", "obtulēre", "obtetulērunt",
        "obtuleram", "obtulerās", "obtulerat", "obtulerāmus", "obtulerātis", "obtulerant",
        "obtulerō", "obtuleris", "obtulerit", "obtulerimus", "obtuleritis",
        "obtulerint", "offeror", "offerris", "offerre", "offertur", "offerimur",
        "offeriminī", "offeruntur", "offerēbar", "offerēbāris", "offerēbāre",
        "offerēbātur", "offerēbāmur", "offerēbāminī", "offerēbantur", "offerar",
        "offerēris", "offerēre", "offerētur", "offerēmur", "offerēminī", "offerentur",
        "offeram", "offerās", "offerat", "offerāmus", "offerātis", "offerant", "offerrem",
        "offerrēs", "offerret", "offerrēmus", "offerrētis", "offerrent", "obtulerim",
        "obtulerīs", "obtulerit", "obtulerīmus", "obtulerītis", "obtulerint", "",
        "obtulissem", "obtulissēs", "obtulisset", "obtulissēmus", "obtulissētis",
        "obtulissent", "", "offerar", "offerāris", "offerāre", "offerātur", "offerāmur",
        "offerāminī", "offerantur", "offerrer", "offerrēris", "offerrēre", "offerrētur",
        "offerrēmur", "offerrēminī", "offerrentur", "offer", "offerte", "offertō",
        "offertōte", "offeruntō", "offerre", "offeriminī", "offertor", "offeruntor",
        "offerendī", "offerendō", "offerendum", "offerendō", "oblātum", "oblātū"
    ] + adjDecl3("offerent", "i"),
    "odi": [
        "odisti", "odit", "odimus", "odistis", "oderunt", "odere",
        "oderam", "oderas", "oderat", "oderamus", "oderatis", "oderant",
        "odero", "oderis", "oderit", "oderimus", "oderitis", "oderint",
        "oderim", "odissem", "odisses", "odisset", "odissemus", "odissetis", "odissent", "odisse", "osurus"
    ] + adjDecl1("osurus"),
    "memini": [
        "meminī", "meministī", "meminit", "meminimus", "meministis", "meminērunt",
        "meminēre",
        "memineram", "meminerās", "meminerat", "meminerāmus", "meminerātis", "meminerant",
        "meminerō", "memineris", "meminerit", "meminerimus", "memineritis", "meminerint",
        "meminerim", "meminerīs", "meminerit", "meminerīmus", "meminerītis", "meminerint",
        "meminissem", "meminissēs", "meminisset", "meminissēmus", "meminissētis", "meminissent", "mementō", "mementōte",
        "meminisse"
    ]
}
