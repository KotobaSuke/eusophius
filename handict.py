import sqlite3
import re
import pandas as pd

hanDict = {}


def parse(raw: str) -> list[tuple]:
    target = []
    varMode = False
    nowToken = ''
    for c in raw + ',':
        if not varMode:
            if c == ',':
                if nowToken: target.append(nowToken)
                nowToken = ''
            elif c == '(':
                varMode = True
                target.append(nowToken)
                nowToken = ''
            else:
                nowToken += c
        else:
            if c == ',':
                target.append('#' + nowToken)
                nowToken = ''
            elif c == ')':
                varMode = False
                target.append('#' + nowToken)
                nowToken = ''
            else:
                nowToken += c
    return target
def cmnIntone(raw: str) -> str:
    if raw[-1] in "1234":
        tone = int(raw[-1])
        raw = raw[:-1]
    else:
        tone = 0

    toneMap = {
        'a': "aāáǎà",
        'e': "eēéěè",
        'i': "iīíǐì",
        'o': "oōóǒò",
        'u': "uūúǔù",
        'v': "üǖǘǚǜ",
        'n': ['n', "n̄", "ń", "ň", "ǹ"],
        'm': ['m', "m̄", "ḿ", "m̌", "m̀"]
    }
    if "iu" in raw:
        raw = raw.replace('u', toneMap['u'][tone])
    elif 'a' in raw:
        raw = raw.replace('a', toneMap['a'][tone])
    elif 'e' in raw:
        raw = raw.replace('e', toneMap['e'][tone])
    elif 'i' in raw:
        raw = raw.replace('i', toneMap['i'][tone])
    elif 'o' in raw:
        raw = raw.replace('o', toneMap['o'][tone])
    elif 'u' in raw:
        raw = raw.replace('u', toneMap['u'][tone])
    elif 'v' in raw:
        raw = raw.replace('v', toneMap['v'][tone])
    elif 'n' in raw:
        raw = raw.replace('n', toneMap['n'][tone])
    elif 'm' in raw:
        raw = raw.replace('m', toneMap['m'][tone])
    if tone == 0: raw = '·' + raw
    return raw
def yueToIPA(yue: str) -> str:
    tone = int(yue[-1])
    yue = yue[:-1] + '#'
    if yue.endswith(('t', 'k', 'p')):
        tone += 6
    yue = yue.replace("ng", 'ŋ')
    ipa = ""
    mapping = {
        'b': 'p',
        'p': "pʰ",
        'm': 'm',
        'f': 'f',
        'd': 't',
        't': "tʰ",
        'n': 'n',
        'l': 'l',
        'ŋ': 'ŋ',
        'g': 'k',
        'k': "kʰ",
        'h': 'h',
        "p#": 'p',
        "t#": 't',
        "k#": "k",
        "gw": "kʷ",
        "kw": "kʷʰ",
        'z': "ts",
        'c': "tsʰ",
        's': 's',
        'j': 'j',
        'w': 'w',
        "ik": "ɪk",
        "iŋ": "ɪŋ",
        "uk": "ʊk",
        "uŋ": "ʊŋ",
        "aa": 'a',
        "yu": 'y',
        "eo": 'ɵ',
        "oe": 'œ',
        'a': 'ɐ',
        'e': 'e',
        'i': 'i',
        'o': 'o',
        'u': 'u',
        '1': "⁵⁵",
        '2': "³⁵",
        '3': "³³",
        '4': "¹¹",
        '5': "²³",
        '6': "²²",
        '7': '⁵',
        '8': '³',
        '9': '²',
        '#': ""
    }
    i = 0
    while i in range(len(yue)):
        if i != len(yue) - 1 and yue[i:i + 2] in mapping:
            ipa += mapping[yue[i:i + 2]]
            i += 2
        else:
            ipa += mapping[yue[i]]
            i += 1
    return '/' + ipa + mapping[str(tone)] + '/'
def yueFormat(rec: str) -> str:
    feed = "　# " if rec.startswith('#') else "\n　　　　　　　　　"
    yue = rec.strip('#')
    return feed + "{}　{}".format(yue, yueToIPA(yue))
def wuuFormat(rec: str) -> str:
    if rec.startswith('|'):
        return '*' + rec.strip('|') + '*'
    else:
        return rec 
def hakToIPA(hak: str) -> str:
    mapping = {
        'p': "pʰ", 'b': 'p',
        't': "tʰ", 'd': 't',
        "ng": 'ŋ',
        'k': "kʰ", 'g': 'k',
        'c': "tsʰ", 'z': "ts",
        "iim": "əm", "iin": "ən", "iib": "əp", "iid": "ət",
        "ii": 'ɿ',
        '1': "⁴⁴", '2': "²²", '3': "³¹", '4': "⁵²", '5': '²', '6': '⁵'
    }
    for k, v in mapping.items():
        hak = hak.replace(k, v)
    return '/' + hak + '/'
def hakFormat(hak: str) -> str:
    feed = "\n　　　　　　　　　"
    return feed + "{}　{}".format(hak, hakToIPA(hak))
def nanIntone(nan: str) -> str:
    for i in range(len(nan)):
        if nan[i] in "1234578":
            break
    tone = int(nan[i])
    nan = nan[:i] + nan[i + 1:]

    nan = nan.replace("iu", "Iu").replace("oo", "oO")
    
    toneMap = {
        'a': ['a', 'á', 'à', 'a', 'â', "", 'ā', "a̍"],
        'e': ['e', 'é', 'à', 'e', 'ê', "", 'ē', "e̍"],
        'o': ['o', 'ó', 'ò', 'o', 'ô', "", 'ō', "o̍"],
        'i': ['i', 'í', 'ì', 'i', 'î', "", 'ī', "i̍"],
        'u': ['u', 'ú', 'ù', 'u', 'û', "", 'ū', "u̍"],
        'm': ['m', "ḿ", "m̀", 'm', "m̂", "", "m̄", ""],
        'n': ['n', "ń", "ǹ", 'n', "n̂", "", "n̄", ""]
    }
    for k, v in toneMap.items():
        if k in nan:
            nan = nan.replace(k, v[tone - 1])
            break
    nan = nan.replace('I', 'i').replace('O', 'o')
    return nan
def nanToIPA(nan: str) -> str:
    nan = nan.strip('*').strip('[').strip(']').strip('(').strip(')').replace("ts",
                                                       'c').replace("nn", 'N')
    nan = nan.replace("ok", "ook").replace("om", "oom").replace("on", "oon")
    ipa = ""
    mapping = {
        'p': 'p',
        "ph": "pʰ",
        'b': 'b',
        'm': 'm',
        't': 't',
        "th": "tʰ",
        'n': 'n',
        'c': "ts",
        "ch": "tsʰ",
        'j': "dz",
        's': 's',
        'l': 'l',
        'k': 'k',
        "kh": "kʰ",
        'g': 'g',
        "ng": 'ŋ',
        'h': 'ʔ',
        'a': 'a',
        'e': 'e',
        'i': 'i',
        'o': 'ə',
        "oo": 'ɔ',
        'u': 'u',
        "aN": "ã",
        "eN": "ẽ",
        "iN": "ĩ",
        "oN": "ɔ̃",
        "uN": "ũ",
        '1': "⁴⁴",
        '2': "⁵¹",
        '3': "³¹",
        '4': '³',
        '5': "²⁴",
        '7': "³³",
        '8': '⁵'
    }
    i = 0
    while i in range(len(nan)):
        if i != len(nan) - 1 and nan[i : i + 2] in mapping:
            ipa += mapping[nan[i : i + 2]]
            i += 2
        else:
            ipa += mapping[nan[i]]
            i += 1
    ipa = ipa.replace("si",
                      "ɕi").replace("zi", "ʑi").replace("ia", "iɛ").replace(
                          "iŋ", "ɪeŋ").replace("ik", "ɪek")
    if ipa.startswith('ʔ'):
        ipa = 'h' + ipa[1:]
    return '/' + ipa + '/'
def nanFormat(rec: str) -> str:
    if rec.startswith(('|', '*')):
        roma = '*' + rec.strip('|') + '*'
    else:
        roma = rec
    feed = "\n　　　　　　　　　"
    return feed + "{}　{}".format(
        nanIntone(roma), ' '.join([nanToIPA(x) for x in roma.split('/')]))
def nanTeoToIPA(nan: str) -> str:
    nan = nan.strip('*').replace("ts", 'c').replace("nn", 'N')
    ipa = ""
    mapping = {
        'p': 'p',
        "ph": "pʰ",
        'b': 'b',
        'm': 'm',
        't': 't',
        "th": "tʰ",
        'n': 'n',
        'c': "ts",
        "ch": "tsʰ",
        'j': "dz",
        's': 's',
        'l': 'l',
        'k': 'k',
        "kh": "kʰ",
        'g': 'g',
        "ng": 'ŋ',
        'h': 'ʔ',
        'a': 'a',
        'e': 'ɛ',
        'i': 'i',
        'o': 'o',
        'u': 'u',
        "aN": "ã",
        "eN": "ẽ",
        "iN": "ĩ",
        "oN": "õ",
        "uN": "ũ",
        '1': "³³",
        '2': "⁵²",
        '3': "²¹³",
        '4': '²',
        '5': "⁵⁵",
        '6': "²⁵",
        '7': "¹¹",
        '8': "⁵⁴"
    }
    i = 0
    while i in range(len(nan)):
        if i != len(nan) - 1 and nan[i : i + 2] in mapping:
            ipa += mapping[nan[i : i + 2]]
            i += 2
        else:
            ipa += mapping[nan[i]]
            i += 1
    if ipa.startswith('ʔ'):
        ipa = 'h' + ipa[1:]
    return '/' + ipa + '/'
def nanTeoFormat(roma: str) -> str:
    feed = "\n　　　　　　　　　"
    return feed + "{}　{}".format(
        nanIntone(roma), ' '.join([nanTeoToIPA(x) for x in roma.split('/')]))
def koDeromanize(roma: str) -> str:
    cons = "bcdfghjklmnprst"
    nucleus = roma.strip(cons)
    iEnd = roma.find(nucleus)
    cStart = iEnd + len(nucleus)
    initial, coda = roma[:iEnd], roma[cStart:]
    initialCode = {
        'g': 0xac00,
        'n': 0xb098,
        'd': 0xb2e4,
        'r': 0xb77c,
        'm': 0xb9c8,
        'b': 0xbc14,
        's': 0xc0ac,
        "ss": 0xc2f8,
        "": 0xc544,
        'j': 0xc790,
        "ch": 0xcc28,
        'k': 0xce74,
        't': 0xd0c0,
        'p': 0xd30c,
        'h': 0xd558
    }[initial]
    nucleusCode = {
        'a': 0x0,
        "ae": 0x1c,
        "ya": 0x38,
        "yae": 0x54,
        "eo": 0x70,
        'e': 0x8c,
        "yeo": 0xa8,
        "ye": 0xc4,
        'o': 0xe0,
        "wa": 0xfc,
        "wae": 0x118,
        "oe": 0x134,
        "yo": 0x150,
        'u': 0x16c,
        "wo": 0x188,
        "we": 0x1a4,
        "wi": 0x1c0,
        "yu": 0x1dc,
        "eu": 0x1f8,
        "ui": 0x214,
        'i': 0x230
    }[nucleus]
    codaCode = {
        "": 0x0,
        'k': 0x1,
        'n': 0x4,
        'l': 0x8,
        'm': 0x10,
        'p': 0x11,
        "ng": 0x15
    }[coda]
    return chr(initialCode + nucleusCode + codaCode)
def koFormat(roma: str) -> str:
    if '(' in roma:
        v1, v2 = roma.strip(')').split('(')
        return "{}({})".format(koDeromanize(v1), koDeromanize(v2))
    else:
        return koDeromanize(roma)
def jaDeromanize(roma: str) -> str:
    roma = roma.replace('*', "**")
    roma = roma.replace('|', '__')
    unigrams = {
        'a': 'あ',
        'i': 'い',
        'u': 'う',
        'e': 'え',
        'o': 'お',
        'n': 'ん',
        'q': 'っ'
    }
    bigrams = {
        "ka": 'か',
        "ki": 'き',
        "ku": 'く',
        "ke": 'け',
        "ko": 'こ',
        "ga": 'が',
        "gi": 'ぎ',
        "gu": 'ぐ',
        "ge": 'げ',
        "go": 'ご',
        "sa": 'さ',
        "si": 'し',
        "su": 'す',
        "se": 'せ',
        "so": 'そ',
        "za": 'ざ',
        "zi": 'じ',
        "zu": 'ず',
        "ze": 'ぜ',
        "zo": 'ぞ',
        "ta": 'た',
        "ti": 'ち',
        "tu": 'つ',
        "te": 'て',
        "to": 'と',
        "da": 'だ',
        "di": 'ぢ',
        "du": 'づ',
        "de": 'で',
        "do": 'ど',
        "na": 'な',
        "ni": 'に',
        "nu": 'ぬ',
        "ne": 'ね',
        "no": 'の',
        "ha": 'は',
        "hi": 'ひ',
        "hu": 'ふ',
        "he": 'へ',
        "ho": 'ほ',
        "ba": 'ば',
        "bi": 'び',
        "bu": 'ぶ',
        "be": 'べ',
        "bo": 'ぼ',
        "pa": 'ぱ',
        "pi": 'ぴ',
        "pu": 'ぷ',
        "pe": 'ぺ',
        "po": 'ぽ',
        "ma": 'ま',
        "mi": 'み',
        "mu": 'む',
        "me": 'め',
        "mo": 'も',
        "ya": 'や',
        "yu": 'ゆ',
        "yo": 'よ',
        "ra": 'ら',
        "ri": 'り',
        "ru": 'る',
        "re": 'れ',
        "ro": 'ろ',
        "wa": 'わ',
        "wi": 'ゐ',
        "we": 'ゑ',
        "wo": 'を'
    }
    trigrams = {
        "kya": "きゃ",
        "kyu": "きゅ",
        "kyo": "きょ",
        "gya": "ぎゃ",
        "gyu": "ぎゅ",
        "gyo": "ぎょ",
        "sya": "しゃ",
        "syu": "しゅ",
        "syo": "しょ",
        "zya": "じゃ",
        "zyu": "じゅ",
        "zyo": "じょ",
        "tya": "ちゃ",
        "tyu": "ちゅ",
        "tyo": "ちょ",
        "dya": "ぢゃ",
        "dyu": "ぢゅ",
        "dyo": "ぢょ",
        "nya": "にゃ",
        "nyu": "にゅ",
        "nyo": "にょ",
        "hya": "ひゃ",
        "hyu": "ひゅ",
        "hyo": "ひょ",
        "bya": "びゃ",
        "byu": "びゅ",
        "byo": "びょ",
        "pya": "ぴゃ",
        "pyu": "ぴゅ",
        "pyo": "ぴょ",
        "mya": "みゃ",
        "myu": "みゅ",
        "myo": "みょ",
        "rya": "りゃ",
        "ryu": "りゅ",
        "ryo": "りょ",
        "kwa": "くわ",
        "kwe": "くゑ",
        "kwi": "くゐ",
        "gwa": "ぐわ",
        "gwe": "ぐゑ",
        "gwi": "ぐゐ"
    }
    for k, v in trigrams.items():
        roma = roma.replace(k, v)
    for k, v in bigrams.items():
        roma = roma.replace(k, v)
    for k, v in unigrams.items():
        roma = roma.replace(k, v)
    return roma
def viDetelex(telex: str) -> str:
    digrams = {
        "aw": 'ă', "aa": 'â', "ee": 'ê',
        "oo": 'ô', "ow": 'ơ', "uw": 'ư',
        "dd": 'đ'
    }
    if telex.endswith(('f', 's', 'r', 'x', 'j')):
        tone = {'f': 1, 's': 2, 'r': 3, 'x': 4, 'j': 5}[telex[-1]]
        telex = telex[:-1]
    else:
        tone = 0
    intone = {
        'a': "aàáảãạ", 'ă': "ăằắẳẵặ", 'â': "âầấẩẫậ",
        'e': "eèéẻẽẹ", 'ê': "êềếểễệ", 'i': "iìíỉĩị",
        'o': "oòóỏõọ", 'ô': "ôồốổỗộ", 'ơ': "ơờớởỡợ",
        'u': "uùúủũụ", 'ư': "ưừứửữự", 'y': "yỳýỷỹỵ"
    }
    for k, v in digrams.items():
        telex = telex.replace(k, v)
    for i in telex:
        if i in intone:
            telex = telex.replace(i, intone[i][tone])
            break
    return telex
def zaToIPA(za: str) -> str:
    za = za.replace("ae", 'A').replace("oe", 'O').replace("ie", 'I').replace("ue", 'U').replace("we", 'W').replace("ng", 'N')

    if za.endswith('z'):
        tone = 2
    elif za.endswith('j'):
        tone = 3
    elif za.endswith('x'):
        tone = 4
    elif za.endswith('q'):
        tone = 5
    elif za.endswith('h'):
        tone = 6
    elif za.endswith(('p', 't', 'k')):
        tone = 7
        za += '#'
        for e in ["ap", "at", "ak", "ep", "et", "ek", "op", "ot", "ok", "ue", "we"]:
            if e in za:
                tone = 9
    elif za.endswith(('b', 'd', 'g')):
        tone = 8
        za += '#'
    else:
        tone = 1
        za += '#'
    za = za[:-1]
    
    ipa = ""

    mapping = {
        'b': 'p', "mb": 'ɓ', 'm': 'm', 'f': 'f', 'v': 'β',
        'd': 'd', "nd": 'ɗ', 'n': 'n', 's': 'θ', 'l': 'l',
        'g': 'k', "gv": "kʷ", 'N': 'ŋ', 'h': 'h', 'r': 'ɣ',
        'c': 'ɕ', 'y': 'j', "ny": 'ɲ', "Nv": "ŋʷ", "by": "bʲ", "gy": "kʲ", "my": "mʲ",

        'p': 'p', 't': 't', 'k': 'k',
        'a': "aː", "ai": "aːi", "au": "aːu",
        'A': "ai", "Au": "au", "aw": "aɯ",
        "Am": "am", "An": "an", "AN": "aŋ",
        "Ap": "ap", "At": "at", "Ak": "ak",
        'e': "eː", "ei": "ei",
        'i': "iː", "I": "iː",
        "im": "im", "in": "in", "iN": "iŋ",
        "ip": "ip", "it": "it", "ik": "ik",
        'o': "oː", "oi": "oːi", "ou": "ou", "O": "o",
        'u': "uː", "ui": "uːi", "U": "uː",
        "um": "um", "un": "un", "uN": "uŋ",
        "up": "up", "ut": "ut", "uk": "uk",
        'w': "ɯː", "wi": "ɯːi", "W": "ɯː",
        "wn": "ɯn", "wN": "ɯŋ", "wt": "ɯt", "wk": "ɯk"
    }
    tones = ["", "²⁴", "³¹", "⁵⁵", "⁴²", "³⁵", "³³", '⁵', "³⁵", '³']
    i = 0
    while i in range(len(za)):
        if i != len(za) - 1 and za[i : i + 2] in mapping:
            ipa += mapping[za[i : i + 2]]
            i += 2
        else:
            ipa += mapping[za[i]]
            i += 1
    ipa += tones[tone]
    return '/' + ipa + '/'
def zaFormat(za: str) -> str:
    feed = "\n　　　　　　　　　"
    return feed + "{}　{}".format(
        za, zaToIPA(za))
def entryFormat(entry: tuple[str, dict[str, list]]) -> str:
    lines = ["**" + entry[0] + "**"]
    val = entry[1]
    if val.get("OCH"):
        lines.append("上古漢語（白沙）：{}".format(", ".join(val["OCH"])))
    if val.get("LTC"):
        lines.append("中古漢語：　　　　{}".format(", ".join(val["LTC"])))
    if val.get("CMN"):
        lines.append("普通話：　　　　　{}".format(", ".join(
            [cmnIntone(x) for x in val["CMN"]])))
    if val.get("YUE"):
        lines.append("粵語（廣州）：　　{}".format("".join(
            [yueFormat(x) for x in val["YUE"]]).lstrip('\n').lstrip('　')))
    if val.get("WUU"):
        lines.append("吳語（上海）：　　{}".format(", ".join(
            [wuuFormat(x) for x in val["WUU"]])))
    if val.get("HAK"):
        lines.append("客家語（梅縣）：　{}".format("".join(
            [hakFormat(x) for x in val["HAK"]]).lstrip('\n').lstrip('　')))
    if val.get("NAN"):
        lines.append("閩南語（臺灣）：　{}".format("".join(
            [nanFormat(x) for x in val["NAN"]]).lstrip('\n').lstrip('　')))
    if val.get("NAN_teo"):
        lines.append("閩南語（潮州）：　{}".format("".join(
            [nanTeoFormat(x) for x in val["NAN_teo"]]).lstrip('\n').lstrip('　')))
    if val.get("KO"):
        lines.append("朝鮮語：　　　　　{}".format(", ".join(
            [koFormat(x) for x in val["KO"]])))
    if val.get("JA_go") or val.get("JA_kan") or val.get("JA_tou"):
        lines.append("日語：　　　" + "（吳）{}".format('/'.join(
            [jaDeromanize(x)
             for x in val.get("JA_go")])) if val.get("JA_go") else "")
        if val.get("JA_kan"):
            lines.append("　　　　　　（漢）{}".format('/'.join(
                [jaDeromanize(x) for x in val.get("JA_kan")])))
        if val.get("JA_tou"):
            lines.append("　　　　　　（唐）{}".format('/'.join(
                [jaDeromanize(x) for x in val.get("JA_tou")])))
        if val.get("JA_ky"):
            lines.append("　　　　　　（慣）{}".format('/'.join(
                [jaDeromanize(x) for x in val.get("JA_ky")])))
        if val.get("JA_x"):
            lines.append("　　　　　　（他）{}".format('/'.join(
                [jaDeromanize(x) for x in val.get("JA_x")])))
    if val.get("VI"):
        lines.append("越南語：　　　　　{}".format(", ".join(
            [viDetelex(x) for x in val["VI"]])))
    if val.get("ZA"):
        lines.append("壯語：　　　　　　{}".format("".join(
            [zaFormat(x) for x in val["ZA"]]).lstrip('\n').lstrip('　')))
    return '\n'.join(lines)


def getEntry(zi: str) -> str:
    if len(zi) != 1:
        return ""
    if zi not in hanDict:
        return ""
    print(hanDict[zi])
    return entryFormat((zi, hanDict[zi]))


def loadDatabase():
    dbfile = "handict_src/mcpdict.db"
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    r = [x for x in cur.execute("SELECT * FROM mcpdict")]
    con.close()

    for e in r:
        zi = chr(int(e[0], 16))
        hanDict[zi] = {}
        if e[1]: hanDict[zi]["LTC"] = e[1].split(',')
        if e[2]: hanDict[zi]["CMN"] = e[2].split(',')
        if e[3]: hanDict[zi]["YUE"] = parse(e[3])
        if e[4]: hanDict[zi]["WUU"] = e[4].split(',')
        if e[5]: hanDict[zi]["NAN"] = e[5].split(',')
        if e[6]: hanDict[zi]["KO"] = e[6].split(',')
        if e[7]: hanDict[zi]["VI"] = e[7].split(',')
        if e[8]: hanDict[zi]["JA_go"] = re.split(r"\[.\]", e[8])[1:] if re.search(r"\[.\]", e[8]) else [e[8]]
        if e[9]: hanDict[zi]["JA_kan"] = re.split(r"\[.\]", e[9])[1:] if re.search(r"\[.\]", e[9]) else [e[9]]
        if e[10]: hanDict[zi]["JA_tou"] = re.split(r"\[.\]", e[10])[1:] if re.search(r"\[.\]", e[10]) else [e[10]]
        if e[11]: hanDict[zi]["JA_ky"] = re.split(r"\[.\]", e[11])[1:] if re.search(r"\[.\]", e[11]) else [e[11]]
        if e[12]: hanDict[zi]["JA_x"] = re.split(r"\[.\]", e[12])[1:] if re.search(r"\[.\]", e[12]) else [e[12]]

    oc = pd.read_csv("handict_src/BSOC.csv").to_numpy().tolist()
    for x in oc:
        zi, prnc = x
        if hanDict.get(zi):
            if hanDict[zi].get("OCH"):
                hanDict[zi]["OCH"].append(prnc)
            else:
                hanDict[zi]["OCH"] = [prnc]
        else:
            hanDict[zi] = {"OCH": [prnc]}

    hakka = pd.read_csv("handict_src/hakka.tsv", sep='\t', header=None).to_numpy().tolist()
    rhyme, initial = None, None
    for l in hakka:
        if l[0].startswith('#'):
            rhyme = l[0][1:]
            continue
        initial = l[0].strip('0')
        for i in l[1:]:
            if str(i) != "nan" and len(i) > 1:
                tone = i[0]
                for zi in i[1:]:
                    prnc = initial + rhyme + tone
                    if hanDict.get(zi):
                        if hanDict[zi].get("HAK"):
                            hanDict[zi]["HAK"].append(prnc)
                        else:
                            hanDict[zi]["HAK"] = [prnc]
                    else:
                        hanDict[zi] = {"HAK": [prnc]}

    teochew = pd.read_csv("handict_src/teochew.tsv", sep='\t', header=None).to_numpy().tolist()
    for x in teochew:
        zi, prnc, note = x[0], x[1], x[3]
        if '文' in note:
            zi = "**" + zi + "**"
        elif '白' in note:
            zi = '*' + zi + '*'
        if hanDict.get(zi):
            if hanDict[zi].get("NAN_teo"):
                hanDict[zi]["NAN_teo"].append(prnc)
            else:
                hanDict[zi]["NAN_teo"] = [prnc]
        else:
            hanDict[zi] = {"NAN_teo": [prnc]}

    zhuang = pd.read_csv("handict_src/zhuang.tsv", sep='\t', header=None).to_numpy().tolist()
    for x in zhuang:
        zi, prnc = x[:2]
        if str(prnc) == "nan": continue
        if hanDict.get(zi):
            if hanDict[zi].get("ZA"):
                hanDict[zi]["ZA"].append(prnc)
            else:
                hanDict[zi]["ZA"] = [prnc]
        else:
            hanDict[zi] = {"ZA": [prnc]}

#char, ltc, cmn, yue, wuu, nan, ko, vi, ja_go, ja_kan, ja_tou, ja_ky, ja_x
