from bs4 import BeautifulSoup, element
from urllib import request, parse
import re
#print(soup)

def escapeFormat(text: str):
  return str(text).replace('*', "\*")

def mainSearch(word: str):
  url = "https://kjjk.weblio.jp/content/{}".format(parse.quote(str(word).encode("utf-8")))
  html = request.urlopen(url)

  rs = {}
  rs["def"] = {"KNKTJ": set(), "KNSYJ": set()}
  soup = BeautifulSoup(html.read(), "html.parser")
  for l in soup.body.find_all('a'):
    if l.attrs.get("name") in ["KNKTJ", "KNSYJ"]:
      consq = list(l.next_siblings)
      for e in consq:
        if e.name == "div" and "kijiWrp" in (e.attrs.get("class") or []):
          rs["head"] = e.contents[1].contents[1].string
          if e.contents[1].contents[3].contents[3].string:
            rs["def"][str(l.attrs.get("name"))].add(e.contents[1].contents[3].contents[3].string)
          if e.contents[1].contents[3].contents[3].contents[0].string:
            rs["def"][str(l.attrs.get("name"))].add(e.contents[1].contents[3].contents[3].contents[0].string)
          try:
            if l.attrs.get("name") == "KNKTJ":
                rs["def"][str(l.attrs.get("name"))] |= set(escapeFormat("".join(list(map(lambda x: x.string, e.contents[1].contents[9].contents[3].contents)))).split(','))
          except:
            pass
          break
    else: continue
  try:
    text = "**{}**".format(rs["head"])
    if rs["def"]["KNKTJ"]:
        text += "\n韓国語単語辞書：　{}".format(', '.join(sorted(rs["def"]["KNKTJ"])))
    if rs["def"]["KNSYJ"]:
        text += "\n韓日専門用語辞書：{}".format(', '.join(sorted(rs["def"]["KNSYJ"])))
    return text
  except:
    return ""