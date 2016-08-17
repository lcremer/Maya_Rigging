
def rigSideSep(text):
    """
    @param text: string to be split by '/'
    @return: returns string array were split by '/' character
    """
    ret = []
    obj = str(text)
    if str(text) == '':
        return ret

    parts = obj.split('/')

    if len(parts) <= 1:
        ret.append(obj)
    else:
        ret.append(parts[len(parts) - 2] + '_')
        ret.append(parts[len(parts) - 1] + '_')
    return ret