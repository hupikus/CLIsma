class worldglobals:
    #performance
    processrate = 30
    framerate = 60
    inputrate = 240

    processdelta = 1 / processrate
    framedelta = 1 / framerate
    inputdelta = 1 / inputrate

    #input
    hold_time = 0.8 #timeout in seconds to differentiate between click and hold
