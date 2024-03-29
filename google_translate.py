import os

os.system("cp utils.py /home/runner/Whatever/venv/lib/python3.10/site-packages/pygoogletranslation/utils.py")

from pygoogletranslation import Translator
# from pygoogletranslation.models import TranslatedPart

def translate(text: str, source: str, dest: str):
  translator = Translator()
  if source == "": source = "la"
  if dest == "": dest = "en"
  codeMapping = {
    "zh": "zh-CN",
    "tzh": "zh-TW"
  }
  if source in codeMapping:
    source = codeMapping[source]
  if dest in codeMapping:
    dest = codeMapping[dest]
  return translator.translate(text, dest=dest, src=source).text

def translateTokenize(cmd: list[str]):
  if '>' in cmd[-1]:
    text = ' '.join(cmd[:-1])
    source, dest = cmd[-1].split('>')
  else:
    text = ' '.join(cmd)
    source, dest = "", ""
  return translate(text, source, dest)