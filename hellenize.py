DASIA = '̔'
PSILI = '̓'
OXIA = '́'
VARIA = '̓̀'
PERISPOMENI = '̃'

LENGTH_MARKED_LETTERS = "ᾱῑῡᾰῐῠ"

LENGTH_NORMALIZATION = {
    "a=": 'ā',
    "e=": 'ē',
    "i=": 'ī',
    "o=": 'ō',
    "y=": 'ȳ',
    "a#": 'ă',
    "i#": 'ĭ',
    "y#": 'y̆',
    "i&": 'ï',
    "y&": 'ÿ',
    "u&": 'ÿ',
    "A=": 'Ā',
    "E=": 'Ē',
    "I=": 'Ī',
    "O=": 'Ō',
    "Y=": 'Ȳ',
    "A#": 'Ă',
    "I#": 'Ĭ',
    "Y#": 'Y̆',
    "I&": 'Ï',
    "Y&": 'Ÿ',
    "U&": 'Ÿ',
}
MONOGRAM_MAPPING = {
    'a': 'α',
    'b': 'β',
    'c': 'κ',
    'd': 'δ',
    'e': 'ε',
    'g': 'γ',
    'i': 'ι',
    'k': 'κ',
    'l': 'λ',
    'm': 'μ',
    'n': 'ν',
    'o': 'ο',
    'p': 'π',
    'r': 'ρ',
    's': 'σ',
    't': 'τ',
    'u': "ου",
    'x': 'ξ',
    'y': 'υ',
    'z': 'ζ',
    'ā': 'ᾱ',
    'ē': 'η',
    'ī': 'ῑ',
    'ō': 'ω',
    'ȳ': 'ῡ',
    'ă': 'ᾰ',
    'ĭ': 'ῐ',
    'y̆': 'ῠ',
    'ï': 'ϊ',
    'ÿ': 'ϋ',
}
BIGRAM_MAPPING = {
    "ch": 'χ',
    "kh": 'χ',
    "ph": 'φ',
    "ps": 'ψ',
    "th": 'θ',
    "rh": 'ῥ',
    "rr": "ρρ",
    "ai": "αι",
    "au": "αυ",
    "ei": "ει",
    "eu": "ευ",
    "oi": "οι",
    "yi": "υι",
    "āi": 'ᾳ',
    "āu": "ᾱυ",
    "ēi": 'ῃ',
    "ēu": "ηυ",
    "ōi": 'ῳ',
    "ōu": "ωυ",
}
TRIGRAM_MAPPING = {
    "rrh": "ρρ",
}
ROUGH_BREATHING = {
    "αι": "\\αἱ",
    "αυ": "\\αὑ",
    "ει": "\\εἱ",
    "ευ": "\\εὑ",
    "οι": "\\οἱ",
    "υι": "\\υἱ",
    "ᾱυ": "\\ᾱὑ",
    "ηυ": "\\ηὑ",
    "ου": "\\οὑ",
    "ωυ": "\\ωὑ",
    'α': 'ἁ',
    'ε': 'ἑ',
    'ι': 'ἱ',
    'ο': 'ὁ',
    'υ': 'ὑ',
    'η': 'ἡ',
    'ω': 'ὡ',
    'ᾳ': 'ᾁ',
    'ῃ': 'ᾑ',
    'ῳ': 'ᾡ',
}
SMOOTH_BREATHING = {
    "αι": "\\αἰ",
    "αυ": "\\αὐ",
    "ει": "\\εἰ",
    "ευ": "\\εὐ",
    "οι": "\\οἰ",
    "υι": "\\υἰ",
    "ᾱυ": "\\ᾱὐ",
    "ηυ": "\\ηὐ",
    "ου": "\\οὐ",
    "ωυ": "\\ωὐ",
    'α': 'ἀ',
    'ε': 'ἐ',
    'ι': 'ἰ',
    'ο': 'ὀ',
    'υ': 'ὐ',
    'η': 'ἠ',
    'ω': 'ὠ',
    'ᾳ': 'ᾀ',
    'ῃ': 'ᾐ',
    'ῳ': 'ᾠ',
}
ACUTE_ACCENTING = {
    'α': 'ά',
    'ε': 'έ',
    'ι': 'ί',
    'ο': 'ό',
    'υ': 'ύ',
    'η': 'ή',
    'ω': 'ώ',
    'ϊ': 'ΐ',
    'ϋ': 'ΰ',
    'ἁ': 'ἅ',
    'ἑ': 'ἕ',
    'ἱ': 'ἵ',
    'ὁ': 'ὅ',
    'ὑ': 'ὕ',
    'ἡ': 'ἥ',
    'ὡ': 'ὥ',
    'ἀ': 'ἄ',
    'ἐ': 'ἔ',
    'ἰ': 'ἴ',
    'ὀ': 'ὄ',
    'ὐ': 'ὔ',
    'ἠ': 'ἤ',
    'ὠ': 'ὤ',
    'ᾳ': 'ᾴ',
    'ῃ': 'ῄ',
    'ῳ': 'ῴ',
    'ᾁ': 'ᾅ',
    'ᾑ': 'ᾕ',
    'ᾡ': 'ᾥ',
    'ᾀ': 'ᾄ',
    'ᾐ': 'ἤ',
    'ᾠ': 'ᾤ',
}
GRAVE_ACCENTING = {
    'α': 'ὰ',
    'ε': 'ὲ',
    'ι': 'ὶ',
    'ο': 'ὸ',
    'υ': 'ὺ',
    'η': 'ὴ',
    'ω': 'ὼ',
    'ϊ': 'ΐ',
    'ϋ': 'ΰ',
    'ἁ': 'ἃ',
    'ἑ': 'ἓ',
    'ἱ': 'ἳ',
    'ὁ': 'ὃ',
    'ὑ': 'ὓ',
    'ἡ': 'ἣ',
    'ὡ': 'ὣ',
    'ἀ': 'ἂ',
    'ἐ': 'ἒ',
    'ἰ': 'ἲ',
    'ὀ': 'ὂ',
    'ὐ': 'ὒ',
    'ἠ': 'ἢ',
    'ὠ': 'ὢ',
    'ᾳ': 'ᾲ',
    'ῃ': 'ῂ',
    'ῳ': 'ῲ',
    'ᾁ': 'ᾃ',
    'ᾑ': 'ᾓ',
    'ᾡ': 'ᾣ',
    'ᾀ': 'ᾂ',
    'ᾐ': 'ᾒ',
    'ᾠ': 'ᾢ',
}
CIRCUMFLEX_ACCENTING = {
    'α': 'ᾶ',
    'ε': 'ῆ',
    'ι': 'ῖ',
    'ο': 'ῶ',
    'υ': 'ῦ',
    'η': 'ῆ',
    'ω': 'ῶ',
    'ϊ': 'ῗ',
    'ϋ': 'ῧ',
    'ἁ': 'ἇ',
    'ἑ': 'ἧ',
    'ἱ': 'ἷ',
    'ὁ': 'ὧ',
    'ὑ': 'ὗ',
    'ἡ': 'ἧ',
    'ὡ': 'ὧ',
    'ἀ': 'ἆ',
    'ἐ': 'ἦ',
    'ἰ': 'ἶ',
    'ὀ': 'ὦ',
    'ὐ': 'ὖ',
    'ἠ': 'ἦ',
    'ὠ': 'ὦ',
    'ᾳ': 'ᾷ',
    'ῃ': 'ῇ',
    'ῳ': 'ῷ',
    'ᾁ': 'ᾇ',
    'ᾑ': 'ᾗ',
    'ᾡ': 'ᾧ',
    'ᾀ': 'ᾆ',
    'ᾐ': 'ᾖ',
    'ᾠ': 'ᾦ',
}
IOTA_SUBSCRIPT_NORMALIZATION = {
    'ᾼ': "Αι",
    'ᾈ': "Ἀι",
    'ᾉ': "Ἁι",
    'ᾊ': "Ἂι",
    'ᾋ': "Ἃι",
    'ᾌ': "Ἄι",
    'ᾍ': "Ἅι",
    'ᾎ': "Ἆι",
    'ᾏ': "Ἇι",
    'ῌ': "Ηι",
    'ᾘ': "Ἠι",
    'ᾙ': "Ἡι",
    'ᾚ': "Ἢι",
    'ᾛ': "Ἣι",
    'ᾜ': "Ἤι",
    'ᾝ': "Ἥι",
    'ᾞ': "Ἦι",
    'ᾟ': "Ἧι",
    'ῼ': "Ωι",
    'ᾨ': "Ὠι",
    'ᾩ': "Ὡι",
    'ᾪ': "Ὢι",
    'ᾫ': "Ὣι",
    'ᾬ': "Ὤι",
    'ᾭ': "Ὥι",
    'ᾮ': "Ὦι",
    'ᾯ': "Ὧι",
}


def latinToGreek(latin: str,
                 initialSmooth: bool = True,
                 upperIotaSubscript: bool = False) -> str:
    rs = ' ' + latin + ' '
    rs = rs.replace("\\`", '`')
    for d in [
            LENGTH_NORMALIZATION, TRIGRAM_MAPPING, BIGRAM_MAPPING,
            MONOGRAM_MAPPING
    ]:
        for (k, v) in d.items():
            rs = rs.replace(k, v)
            rs = rs.replace(k.upper(), v.upper())
            rs = rs.replace(k.title(), v.title())

    for (k, v) in ROUGH_BREATHING.items():
        rs = rs.replace('h' + k, v)
        rs = rs.replace('H' + k, v.title())
        rs = rs.replace('H' + k.title(), v.title())
        rs = rs.replace('H' + k.upper(), v.upper())

    for (k, v) in SMOOTH_BREATHING.items():
        rs = rs.replace(k + '>', v)
        rs = rs.replace(k.upper() + '>', v.upper())
        if initialSmooth:
            rs = rs.replace(' ' + k, ' ' + v)
            rs = rs.replace('\n' + k, '\n' + v)
            rs = rs.replace(' ' + k.title(), ' ' + v.title())
            rs = rs.replace('\n' + k.title(), '\n' + v.title())
            rs = rs.replace(' ' + k.upper(), ' ' + v.upper())
            rs = rs.replace('\n' + k.upper(), '\n' + v.upper())

    for e in ACUTE_ACCENTING:
        rs = rs.replace(e + ';', ACUTE_ACCENTING[e])
        rs = rs.replace(e.upper() + ';', ACUTE_ACCENTING[e].upper())
        rs = rs.replace(e + '`', GRAVE_ACCENTING[e])
        rs = rs.replace(e.upper() + '`', GRAVE_ACCENTING[e].upper())
        if e in CIRCUMFLEX_ACCENTING:
            rs = rs.replace(e + '^', CIRCUMFLEX_ACCENTING[e])
            rs = rs.replace(e.upper() + '^', CIRCUMFLEX_ACCENTING[e].upper())

    for e in LENGTH_MARKED_LETTERS:
        rs = rs.replace(e + ';', e + OXIA)
        rs = rs.replace(e.upper() + ';', e.upper() + OXIA)
        rs = rs.replace(e + '`', e + VARIA)
        rs = rs.replace(e.upper() + '`', e.upper() + VARIA)
        rs = rs.replace(e + '^', e + PERISPOMENI)
        rs = rs.replace(e.upper() + '^', e.upper() + PERISPOMENI)
        rs = rs.replace('h' + e, e + DASIA)
        rs = rs.replace('H' + e.upper(), e.upper() + DASIA)
        if initialSmooth:
            rs = rs.replace(' ' + e, ' ' + e + PSILI)
            rs = rs.replace('\n' + e, '\n' + e + PSILI)
            rs = rs.replace(' ' + e.upper(), ' ' + e.upper() + PSILI)
            rs = rs.replace('\n' + e.upper(), '\n' + e.upper() + PSILI)

    if not upperIotaSubscript:
        for (k, v) in IOTA_SUBSCRIPT_NORMALIZATION.items():
            rs = rs.replace(k, v)

    rs = rs.replace(':', '·')
    rs = rs.replace("σ ", "ς ")
    rs = rs.replace("σ.", "ς.")
    rs = rs.replace("σ·", "ς·")
    rs = rs.replace("σ,", "ς,")
    rs = rs.replace("σ!", "ς!")
    rs = rs.replace("σ;", "ς;")
    rs = rs.replace("\σ", 'ς')
    rs = rs.replace("\ς", 'σ')
    rs = rs.replace('\'', '᾽')
    rs = rs.replace("\\", "")
    return rs[1:-1]

def help():
    helpText = [
        "**α**: *a*, **ε**: *e*, **ι**: *i*, **ο**: *o*, **υ**: *y*, **η**: *e=*, **ω**: *o=*",
        "**β**: *b*, **γ**: *g*, **δ**: *d*, **ζ**: *z*, **θ**: *th*, **κ**: *c/k*, **λ**: *l*",
        "**μ**: *m*, **ν**: *n*, **ξ**: *x*, **π**: *p*, **ρ**: *r*, **σ**: *s*, **τ**: *t*, **φ**: *ph*, **χ**: *ch/kh*, **ψ**: *ps*",
        "**αι**: *ai*, **ει**: *ei*, **οι**: *oi*, **υι**: *yi*, **αυ**: *au*, **ευ**: *eu*, **ου**: *u* *(not ou)*",
        "**ᾳ**: *a=i*, **ῃ**: *e=i*, **ῳ**: *o=i*",
        "equal sign(=) for long vowel, hash mark(#) for short vowel (only for α, ι, υ)",
        "first vowel in short diphthong + equal sign = long diphthong, e.g. **ᾱυ**: *a=u*",
        "initial vowel with smooth breath mark by default, `-p` to disable",
        "iota subscript becomes adscript when capitalized, `-i` to keep subscript",
        "h + vowel for rough breath, but **ῥ**: *rh*",
        "semicolon(;) for acute accent, grave sign(\` or \\\`) for grave, caret(^) for circumflex",
        "η and ω with circumflex do not require equal sign, e.g. **ῆ**: *e^*",
        "ampersand(&) for diaraesis, written before accent mark",
        "final σ becomes ς by default, backslash to convert σ/ς",
        "larger sign(>) for forced smooth breath mark/coronis",
        "colon(:) turns to middot(·)"
    ]
    return '\n'.join(helpText)