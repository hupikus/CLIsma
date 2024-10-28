class Loghandler:

    loglen = 0
    history = []

    #preferences
    MaxLen = 25

    @staticmethod
    def Log(msg):
        Loghandler.history.append(msg)
        if Loghandler.loglen < Loghandler.MaxLen:
            Loghandler.loglen += 1
        else:
            Loghandler.history.pop(0)