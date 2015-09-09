letters = {
    ' ':'1',
    'e':'10',
    't':'11',
    'a':'101',
    'o':'110',
    'i':'111',
    'n':'1010',
    's':'1011',
    'h':'1101',
    'r':'1110',
    'd':'1111',
    'l':'10101',
    'c':'10110',
    'u':'10111',
    'm':'11010',
    'w':'11011',
    'f':'11101',
    'g':'11110',
    'y':'11111',
    'p':'101011',
    'b':'101101',
    'v':'101110',
    'k':'101010',
    'j':'101111',
    'x':'110101',
    'q':'110111',
    'z':'111010',
    '0':'111101',
    '1':'111110',
    '2':'111111',
    '3':'1010101',
    '4':'1010111',
    '5':'1011010',
    '6':'1011011',
    '7':'1011101',
    '8':'1011110',
    '9':'1011111',
    'en':'1101010',
    're':'1101011',
    'er':'1101101',
    'nt':'1101110',
    'th':'1101111',
    'on':'1110101',
    'in':'1110110',
    'te':'1110111',
    'an':'1111010',
    'or':'1111011',
    'st':'1111101',
    'ed':'1111110',
    'ne':'1111111',
    'he':'10101010',
    'ee':'10101011',
    'tt':'10101101',
    'oo':'10101110',
    'ss':'10101111',
    'll':'10110101',
    'ff':'10110110'
    }

bits = {}
for i in letters:
    bits[letters[i]] = i

def compress(m):
    m = m.lower()
    output = ""
    i = 0
    while (i < len(m)):
        if (i < len(m) - 1 and m[i:i + 2] in letters):
            output += letters[m[i:i + 2]]
            i += 2
        elif (m[i] in letters):
            output += letters[m[i]]
            i += 1
        else:
            print "Missing letter"
            i += 1
        output += "00"
    return output

def decompress(m):
    current = ""
    output = ""
    for i in m:
        current += i
        if (current[len(current) - 3:len(current)] == '001'):
            output += bits[current[:len(current) - 3]]
            current = "1"
    if (len(current) > 0):
        output += bits[current[:len(current) - 2]]
    return output.upper()

def test(msg):
    x = len(msg)
    print 'MESSAGE: ' + msg
    print 'Read Message of {} Bytes.'.format(x)
    y = compress(msg)
    print 'Compressing {} Bits into {} Bits. ({}% compression)'.format(x * 8, len(y), 100*(8 * x - float(len(y))) / (x * 8))
    print 'Sending Message.'
    print 'Decompressing Message into {} Bytes.'.format(x)
    if (decompress(y) == msg):
        print 'Message Matches!'
    else:
        print decompress(y)
        print 'Message send failure!'

def main():
    for i in ['REMEMBER TO DRINK YOUR OVALTINE', 'GIANTS BEAT DODGERS 10 TO 9 AND PLAY TOMORROW AT 1300 ', 'SPACE THE FINAL FRONTIER THESE ARE THE VOYAGES OF THE BIT STREAM DAILY PROGRAMMER TO SEEK OUT NEW COMPRESSION']:
        test(i)
        print "\n"
 
if __name__ == '__main__':
    main()
