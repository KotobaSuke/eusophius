import random

def greet(hour: int):
  morningGreets = [
    "Tempus matutinum est. Quid ages hodie?",
    "Salve, bonum diem habeas!",
    "ὑπίαινε! Quid ages hodie?",
    "χαῖρε πολλά!"
  ]
  noonGreets = [
    "Tempus est ad prandium adducendum.",
    "Mmm, quale est prandium hodie?",
    "χαῖρε!",
    "Mmm, esurio. Quando ad prandium ibimus?"
  ]
  afternoonGreets = [
    "Quid agis?",
    "χαῖρε!",
    "Mmm, me vocas?",
    "Eh?"
  ]
  eveningGreets = [
    "Eh? Tempus cenandum est.",
    "Salve!",
    "Quid agis?"
  ]
  nightGreets = [
    "Quid agis hac nocte?",
    "Salve et tu! Habesne bene hac nocte?"
  ]
  lateNightGreets = [
    "Nunc sera nocte est. Bene valeas et quiescas.",
    "Serum est. Bene quiescas!",
    "ὑπίαινε! Mecum cras ludas!"
  ]
  midnightGreets = [
    "Zzz..."
  ]
  
  if hour in range(5, 10):
    greets = morningGreets
  elif hour in range(10, 13):
    greets = noonGreets
  elif hour in range(13, 18):
    greets = afternoonGreets
  elif hour in range(18, 20):
    greets = eveningGreets
  elif hour in range(20, 22):
    greets = nightGreets
  elif hour in range(23, 24):
    greets = lateNightGreets
  elif hour in range(0, 5):
    greets = midnightGreets

  return random.choice(greets)
    