def picGen(pic):
    lines = pic.split()
    for i in lines:
        b = "{0:08b}".format(int(i, 16))
        for j in b:
            if (j == "0"):
                print " ",
            elif (j == "1"):
                print "X",
        print "\n",

for i in ["FF 81 BD A5 A5 BD 81 FF", "AA 55 AA 55 AA 55 AA 55", "3E 7F FC F8 F8 FC 7F 3E", "93 93 93 F3 F3 93 93 93"]:
    picGen(i)
    print "\n"