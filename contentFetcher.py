import random

def getQuotes(filename):
    quotes = []
    with open('./data/'+filename) as f:
        lines = f.readlines()
        quote = ""
        for i, line in enumerate(lines):
            if i % 4 == 0:
                quote = line.strip()
            elif i % 2 == 0:
                quote += "\n" + line.strip()
                quotes.append(quote)
                quote = ""
    f.close()
    return quotes

def getRandom(filename):
    quotes = getQuotes(filename)
    return(quotes[random.randint(0, len(quotes))])





