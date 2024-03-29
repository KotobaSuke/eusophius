from replit import db
from inflection import extractName

def getUserName(rawName: str, shear: bool=False) -> str:
    if rawName in db["username"].keys():
        return db["username"][rawName]
    else:
        return extractName(rawName, shear)

def setUserName(rawName: str, newName: str) -> str:
    if "username" in db.keys():
        db["username"][rawName] = newName
    else:
        db["username"] = {}

def delUserName(rawName: str) -> None:
    try:
        del db["username"][rawName]
    except:
        pass