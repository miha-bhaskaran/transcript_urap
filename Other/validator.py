import csv


def outWholeLine(original, compare):

    with open(compare, "r") as t1, open(original, "r") as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    with open("update.csv", "w") as outFile:
        for line in filetwo:
            if line not in fileone:
                outFile.write(line)


def outCharDiff(original, compare):

    with open(compare, "r") as t1, open(original, "r") as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    with open("outCharDiff.csv", "w", newline="") as outFile:
        writer = csv.writer(outFile)
        for i in range(len(filetwo)):
            line = filetwo[i]
            if line not in fileone:
                difference = len(
                    line.strip()
                )  # strip() removes leading/trailing whitespace
                writer.writerow([i, difference])


original = "validation/trans_val.csv"
compare = "trans.png.csv"

# outWholeLine(original, compare)
outCharDiff(original, compare)
