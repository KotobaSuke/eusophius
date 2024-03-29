from datetime import *
import hashlib
import random

def countFortuneCrypt(tag: int):
  nowTime = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
  year = nowTime.year
  month = nowTime.month
  day = nowTime.day

  hex = hashlib.md5(str(5 * tag + 3 * year + 2 * month + day).encode()).hexdigest()
  return int(hex, 16)

def countFortune(tag: int):
  return countFortuneCrypt(tag) % 101

def doAndDont(tag: int):
  events = ["Dormire", "Pensum", "Telephono Ludere", "Mathematica", "Legere", "Pingere", "Cantùs Audire", "Exercitium Corporis", "Scribere", "Iter", "Cantùs Facere", "Cantare", "Saltare", "Physica", "Chemia", "Biologia", "Geographia", "Astronomia", "*nihil*", "Nihil Facere", "Instrumenta Canere", "KFC", "McDonald's", "Saizeriya", "Fabulari", "Cinematographi", "Dramata TV", "Laborare", "Convivium", "Raedam Agere", "Navigare", "Lingua Latina", "Lingua Graeca", "Lingua Japonica", "Lingua Francica", "Lingua Anglica", "Lingua Coreana", "Lingua Norvegica", "Emptionem Facere", "Photographare", "Feles Mulcere", "Canes Mulcere", "VOCALOID", "Computatro Ludere", "Temeta Bibere", "Capillos Recidere", "Programmatatio", "Vendere"]
  doEvent = events[countFortuneCrypt(tag) // 100 % len(events)]
  dontEvent = events[countFortuneCrypt(tag) // 100 // len(events) % len(events)]
  if doEvent == dontEvent:
    dontEvent = events[(countFortuneCrypt(tag) % 100 % len(events) + 1)% len(events)]
  return (doEvent, dontEvent)

def dice(face: int):
  return random.randint(1, face)