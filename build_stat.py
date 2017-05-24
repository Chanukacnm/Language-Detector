import string
import sys

# Meta Data
data = []
vSet = ['a', 'e', 'i', 'o', 'u']
cSet = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
cvCombinations = {}
cvvCombinations = {}

totalLetters = 0
cvcvvCount = {'cv' : {}, 'cvv' : {}}
letterCounts = {}
cvCount = 0
cvvCount = 0


def initializeStats():
    global cSet, vSet, cvcvvCount, alphabet, letterCounts, cvCount, cvvCount

    for l in alphabet:
        letterCounts[l] = 0

    for c in cSet:
        for v1 in vSet:
            cvcvvCount['cv'][c + v1] = 0
            cvCount += 1
            for v2 in vSet:
                cvcvvCount['cvv'][c + v1 + v2] = 0
                cvvCount += 1


# Reading data and obtaining the array of data
def readData(fileName):
    global totalLetters
    print "Operation Started!!"
    with open (fileName, "r") as f:
        for line in f:
            data = ' '.join([l.strip() for l in line.split()])
            # Cleaning data
            data = data.translate(string.maketrans("",""), string.punctuation)
            dataArray = data.strip().split()

            # Exectute data generation for each word
            for word in dataArray:
                if len(word) == 0: continue
                totalLetters+= len(word)
                word = word.lower()
                cvSet(word)
                cvvSet(word)
                letterCount(word)
    print "Operation Completed!!"
            

            # return dataArray

# Get the set if CV set for a word
def cvSet(word):
    global vSet, cSet, cvCount
    for i in range(len(word)-1):
        c, v = word[i], word[i+1]
        if v in vSet and c in cSet:
            key = c + v
            cvcvvCount['cv'][key] += 1
            cvCount += 1
    return True


# Get the set of CVV set for a word
def cvvSet(word):
    global vSet, cSet, cvcvvCount, cvvCount
    for i in range(len(word)-2):
        c, v1, v2 = word[i], word[i+1], word[i+2]
        if v1 in vSet and v2 in vSet and c in cSet:
            key = c + v1 + v2
            cvcvvCount['cvv'][key] += 1
            cvvCount += 1

    return True

# Get the letter count
def letterCount(word):
    global letterCounts
    for i in word:
        letterCounts[i] += 1
    return True


initialData = sys.argv

if len(initialData) != 3:
    print "Use python build_stat.py <LANGUAGE DATA> <TARGET DATA>"
else:
    targetFilename = initialData[2]
    dataFilename = initialData[1]

    # Initializing stat data
    initializeStats()
    print 'Initialized stat data'
    # Excecute algorithm
    readData(dataFilename)
    with open(targetFilename, 'wb') as f:
        f.writelines("totalLetters: " + str(totalLetters))
        f.writelines("\nletterCounts: " + str(letterCounts))
        f.writelines("\ncvCount: " + str(cvCount))
        f.writelines("\ncvvCount: " + str(cvvCount))
        f.writelines("\ncvcvvCount: " + str(cvcvvCount))
    # Write information on to a file
