from PIL import Image
import os

def main():
    pbmfile = raw_input("Which pbm file to display?\n>> ")
    pbmfile = pbmfile.upper() + '.pbm'
    if not os.path.isfile(os.getcwd() + "\\" + pbmfile):
        print "File does not exist!"
        return
    with open(pbmfile, 'r') as f:
        pbmformat = f.readline()
        dimensions = tuple(int(n) for n in f.readline().split())
        output = []
        for _ in range(0, dimensions[1]):
            output.append(f.readline().split())
        f.close()
        for i in output:
            i[-1] = i[-1][:1]
    im = Image.new("RGB", dimensions, None)
    pixels = im.load()
    for y, row in enumerate(output):
        for x, char in enumerate(row):
            if char == "1":
                pixels[x, y] = (0, 0, 0)
            elif char == "0":
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (128, 128, 128)
    im.show()
    im.save(os.getcwd() + "\\" + pbmfile[:-4] + ".png", 'PNG')

if __name__ == '__main__':
    main()