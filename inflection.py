def extractName(name: str, shear: bool=False) -> str:
    if ' ' in name:
        return name.split(' ')[1]
    elif '_' in name:
        return name.split('_')[1]
    else:
        if len(name) > 10 and shear:
            return name[:9] + '…'
        else:
            return name

def vocativize(name: str) -> str:
  if name.endswith("ius"):
    return name[:-2]
  elif name.endswith("us"):
    return name[:-2] + 'e'
  elif name.endswith("as"):
    return name[:-1]
  else:
    return name