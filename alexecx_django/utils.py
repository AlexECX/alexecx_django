import unicodedata

def unaccent(string):
    try:
        unicode(string, 'utf-8')
    except NameError:
        pass
    return str(unicodedata\
        .normalize('NFD', string)\
        .encode('ascii', 'ignore')\
        .decode('utf-8'))    