letters = {}

with open('txt2pic.txt', 'r') as f:
    lines = f.readlines()
    f.close()

for i in range(0, 26):
    letters[lines[8 * i][:1]] = []
    for j in range (1, 8):
        letters[lines[8 * i][:1]].append(lines[8 * i + j][:len(lines[8 * i + j]) - 1])
letters[" "] = ["0 0 0 0 0", "0 0 0 0 0", "0 0 0 0 0", "0 0 0 0 0", "0 0 0 0 0", "0 0 0 0 0", "0 0 0 0 0"]

def main():
    print "Input text for image: "
    text = raw_input('>> ')
    text = text.upper()
    for l in text:
        if l not in letters:
            print "Invalid character: " + l
            return
    output = ["","","","","","",""]
    for l in text:
        for row in range(0, 7):
            output[row] += letters[l][row] + " 0 "
    with open(text + ".pbm", 'w+') as f:
        f.write("P1\n")
        f.write(str(len(output[0]) / 2) + " 7\n")
        for row in range(0,7):
            f.write(output[row] + "\n")
        f.close()
if __name__ == '__main__':
    main()