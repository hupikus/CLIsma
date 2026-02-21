class Loghandler:

    loglen = 0
    history = []

    # Preferences
    MaxLen = 50

    @staticmethod
    def Log(msg):
        Loghandler.history.append(str(msg).replace('\n', ''))
        if Loghandler.loglen < Loghandler.MaxLen:
            Loghandler.loglen += 1
        else:
            Loghandler.history.pop(0)

# In case developer makes a typo
class Lolhandler:

    @staticmethod
    def Log(msg):
        raise TypoException('"Lol" expected, got "Log". Did you mean "Lolhandler.Lol()?"')

    @staticmethod
    def Lol(msg):
        l = len(str(msg))
        s = ('LO' * (l // 2))
        if l & 1:
            s += 'L'
        Loghandler.Log(s)

class TypoException(Exception):
    pass
