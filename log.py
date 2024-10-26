class loghandler:

    loglen = 0
    history = []

    #preferences
    MaxLen = 25

    @staticmethod
    def Log(msg):
        history.append(msg)
        if loglen < MaxLen:
            loglen += 1
        else:
            history.pop(0)