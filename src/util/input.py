
def readFromFile(filename:str, strip:bool=False) -> list[str]:
    with open(filename, 'r') as f:
        out = f.readlines()
        if strip:    
            out = list(map(lambda x: x.strip(), out))
        return out
