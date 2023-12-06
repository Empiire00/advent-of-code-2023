
def readFromFile(filename: str, strip: bool = False) -> list[str]:
    with open(filename, 'r') as f:
        out = f.readlines()
        if strip:
            out = list(map(lambda x: x.strip(), out))
        return out


def read_from_file_to_string(filename: str, strip: bool = False) -> str:
    with open(filename, 'r') as f:
        out = f.read()
        if strip:
            out = out.strip()
        return out
