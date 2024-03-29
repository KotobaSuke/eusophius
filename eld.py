from bs4 import BeautifulSoup, element
from urllib import request
import re

#print(soup)


def getChildrenByName(node, name: str):
  try:
    return list(filter(lambda x: x.name == name, node.contents))
  except:
    return ["WRONG"]


def escapeFormat(text: str):
  return str(text).replace('*', "\*")


def embolden(text: str):
  return "**{}**".format(text)


def italicize(text: str):
  return "*{}*".format(text)


def mainSearch(word: str):
  url = "https://www.perseus.tufts.edu/hopper/text?doc={}&fromdoc=Perseus%3Atext%3A1999.04.0060".format(
    word)
  html = request.urlopen(url)
  try:
    rs = {}
    soup = BeautifulSoup(html.read(), "html.parser")
    for l in soup.body.find_all("div"):
      if l.attrs.get("class") and "text" in l.attrs.get("class"):
        c = list(l.children)
        offset = 0
        try:
          rs["head"] = embolden(str(c[0].contents[0].contents[0].contents[0].string))
        except:
          rs["head"] = embolden(str(c[0].contents[1].contents[0].contents[0].string))
          offset = 1
        rs["infl"] = italicize(re.sub(r'[\n ]+', " ",str(c[0].contents[1 + offset]).strip()))
        rs["note"] = ""
        rs["def"] = ""
        defText = c[0].contents[2 + offset].contents
        for e in defText:
          if isinstance(e, element.NavigableString):
            pass
            '''if "—" in str(e):
            rs["def"] += "\n" + escapeFormat(e).split("—")[1].strip()[:-1]'''
          elif isinstance(e, element.Tag):
            if e.name == "strong":
              if e.string == "comp.":
                rs["note"] += italicize(escapeFormat(e.string))
            elif e.name == "span" and "greek" in e.attrs.get("class"):
              rs["note"] += " " + escapeFormat(e.contents[0].contents[0])
            elif e.name == 'i' and not rs["def"]:
              rs["def"] += "\n" + escapeFormat(e.string).strip().removesuffix(':')
  
    text = "{}  {}  {}\n{}\n".format(rs["head"], rs["infl"],
            '(' + rs["note"].strip() + ')' if rs["note"] else "", rs["def"])
    return text
  except:
    return ""