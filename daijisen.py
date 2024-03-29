from bs4 import BeautifulSoup, element
from urllib import request, parse
import re
#print(soup)


def escapeFormat(text: str):
    return str(text).replace('*', "\*")


def mainSearch(word: str):
    url = "https://www.weblio.jp/content/{}".format(
        parse.quote(str(word).encode("utf-8")))
    html = request.urlopen(url)

    rs = {}
    soup = BeautifulSoup(html.read(), "html.parser")
    for l in soup.body.find_all('a'):
        if l.attrs.get("name") == "SGKDJ":
            consq = list(l.next_siblings)
            for e in consq:
                if e.name == "div" and "kijiWrp" in (e.attrs.get("class")
                                                     or []):
                    rs["head"] = escapeFormat("".join(
                        list(map(lambda x: x.string,
                                 e.contents[1].contents[1]))))
                    #detagger = lambda x: x.string if isinstance(x, element.NavigableString) else (detagger(x) if isinstance(x, element.Tag) else "")
                    rs["class"] = ""
                    try:
                        rs["class"] = "".join(
                            list(
                                map(
                                    lambda x: x.string,
                                    e.contents[1].contents[3].contents[2].
                                    contents[0].contents)))
                        offset = 2
                        if not rs["class"].startswith('［'):
                            rs["class"] = ""
                            offset = 0
                        rs["def"] = []
                        for i in range(0, 100, 2):
                            try:
                                f = e.contents[1].contents[3].contents[2 +
                                                                       offset +
                                                                       i]
                            except:
                                break
                            if isinstance(f, element.Tag) and f.name == "p":
                                defText = escapeFormat("".join(
                                    list(map(lambda x: x.string, f.contents))))
                                if not defText.startswith("[下接語]"):
                                    rs["def"].append(defText)
                    except:
                        f = e.contents[1].contents[3].contents[2].contents
                        rs["def"] = [
                            escapeFormat("".join(
                                list(map(lambda x: x.string, f))))
                        ]
                    break
    try:
        text = "**{}**  {}\n{}".format(rs["head"], rs["class"],
                                       '\n'.join(rs["def"]))
        return text
    except:
        return ""
