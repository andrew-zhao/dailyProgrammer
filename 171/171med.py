def picGen(pic):
    lines = pic.split()
    output = []
    for i in lines:
        newLine = ""
        b = "{0:08b}".format(int(i, 16))
        for j in b:
            if (j == "0"):
                newLine += " "
            elif (j == "1"):
                newLine += "X"
        output.append(newLine)
    return output

def zoomIn(pic, z):
    if (z != 2 and z != 4):
        print "Zoom must be 2x or 4x"
        return
    output = []
    for i in pic:
        newLine = ""
        for j in i:
            for _ in range(0, z):
                newLine += j
        for _ in range(0,z):
            output.append(newLine)
    return output

def zoomOut(pic, z):
    if (z != 2 and z != 4):
        print "Zoom must be 2x or 4x"
        return
    output = []
    for i in pic[::z]:
        newLine = ""
        for j in i[::z]:
            newLine += j
        output.append(newLine)
    return output

def rotate(pic, d):
    if (d % 90 != 0):
        print "Must be rotated by a multiple of 90 degrees"
        return
    d = (((d % 360) + 360) % 360) / 90
    for i in range(0, d):
        output = []
        for i in range(0, len(pic)):
            newLine = ""
            for j in pic[::-1]:
                newLine += j[i]
            output.append(newLine)
        pic = output
    return pic

def invert(pic):
    output = []
    for i in pic:
        newLine = ""
        for j in i:
            if (j == "X"):
                newLine += " "
            else:
                newLine += "X"
        output.append(newLine)
    return output

for i in ["FF 81 BD A5 A5 BD 81 FF", "AA 55 AA 55 AA 55 AA 55", "3E 7F FC F8 F8 FC 7F 3E", "93 93 93 F3 F3 93 93 93"]:
    a = picGen(i)
    for j in a:
        print j
    print "\n"
    a = zoomIn(a, 4)
    for z in a:
        print z
    print "\n"
    a = zoomOut(a, 4)
    for z in a:
        print z
    print "\n"
    a = rotate(a, 90)
    for z in a:
        print z
    print "\n"
    a = invert(a)
    for z in a:
        print z
    print "\n"