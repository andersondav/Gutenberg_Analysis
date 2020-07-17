#!/usr/bin/python3

import sys, string, re, random
from collections import defaultdict
import heapq

if len(sys.argv) != 2:
    print('Usage: analysis.py <file_name.txt>')
    exit()
try:
    file = open(sys.argv[1])
except:
    print('Unable to open file.')
    exit()

chapter_match = 'CHAPTER [IVX]*\.\n'
regex = re.compile(chapter_match)

punc = []
for c in string.punctuation:
    if c != '\'':
        punc.append(c)
print(punc)
punc_set = set(punc)
punc = ''.join(punc)

def getNumLines():
    lineCount = 0
    for line in file:
        lineCount += 1
    return lineCount
num_lines = getNumLines()

def getTotalNumberOfWords():
    file.seek(0)
    wordCount = 0
    for line in file:
        wordCount += len(line.split())

    return wordCount

def cleanLine(line):
    line = line.translate(str.maketrans('', '', punc))
    return line

def getTotalUniqueWords():
    file.seek(0)
    unique = set()
    for line in file:
        line = cleanLine(line)
        for word in line.split():
            unique.add(word.lower())
    return len(unique)

def getCommonWords(n):
    if n > 1000:
        n = 1000
    common_words = set()
    common = open('common.txt')
    while n > 0:
        word = common.readline().strip('\n')
        common_words.add(word.lower())
        n -= 1
    return common_words

def get20Most(filter, order):
    file.seek(0)
    freqs = defaultdict(int)
    if filter:
        common_words = getCommonWords(100)
    else:
        common_words = set()

    for line in file:
        line = cleanLine(line)
        for word in line.split():
            lowered = word.lower()
            if lowered not in common_words:
                freqs[lowered] += 1
    
    l = []
    for (word, freq) in freqs.items():
        l.append((order * freq, word))
    
    heapq.heapify(l)
    res = []
    for i in range(20):
        (freq, word) = heapq.heappop(l)
        res.append([word, order * freq])
    return res

def get20MostFrequentWords():
    return get20Most(False, -1)

def get20MostInterestingFrequentWords():
    return get20Most(True, -1)

def get20LeastFrequentWords():
    return get20Most(False, 1)

def getFrequencyOfWord(word):
    file.seek(0)
    word = word.lower()

    foundChapterOne = False
    result = []
    curCount = 0
    total = 0
    for line in file:
        if regex.match(line):
            if foundChapterOne:
                result.append(curCount)
                curCount = 0
            else:
                curCount = 0
                foundChapterOne = True
        else:
            for w in cleanLine(line).split():
                if w.lower() == word:
                    curCount += 1
                    total += 1
    return result

def readWord():
    foundFirstChar = False
    word = []
    while not foundFirstChar:
        c = file.read(1)
        if c == ' ' or c == '\n':
            continue
        else:
            word.append(c)
            foundFirstChar = True
    
    while True:
        c = file.read(1)
        if c == ' ' or c == '\n':
            break
        else:
            word.append(c)
    
    return ''.join(word).lower()


def getChapterQuoteAppears(quote):
    file.seek(0)

    quote = quote.lower()
    words = quote.split()

    foundChapterOne = False
    curChapter = 0
    quote_ind = 0
    lineNum = 0
    
    while lineNum < num_lines:
        # print(f'about to read line')
        line_start = file.tell()
        line = file.readline()
        if regex.match(line):
            # this line marks new chapter
            # print(f'chapter {curChapter}')
            if foundChapterOne:
                curChapter += 1
            else:
                foundChapterOne = True
                curChapter = 1
        else:
            # line doesn't mark new chapter,
            # so check starting from each word in line
            for word_start in range(len(line.split())):
                file.seek(line_start)
                for i in range(word_start):
                    readWord()

                while quote_ind < len(words) and readWord() == words[quote_ind]:
                    # print(f'found "{words[quote_ind]}"!')
                    quote_ind += 1
                if quote_ind == len(words):
                    return curChapter
                else:
                    quote_ind = 0
        lineNum += 1
    return -1

def getWord():
    foundFirstChar = False
    word = []
    while not foundFirstChar:
        c = file.read(1)
        if len(c) != 1:
            return None
        elif c == ' ' or c == '\n':
            continue
        else:
            word.append(c)
            foundFirstChar = True
    
    while True:
        c = file.read(1)
        if c == ' ' or c == '\n' or len(c) != 1:
            break
        else:
            word.append(c)
    
    return ''.join(word)

def generateSentence():
    curWords = ['The']
    for i in range(19):
        file.seek(0)
        potentialNexts = []
        while True:
            word = getWord()
            if word == None:
                break
            if word.lower() == curWords[-1].lower():
                nextWord = getWord()
                if nextWord != None:
                    potentialNexts.append(nextWord)
                else:
                    break
        curWords.append(potentialNexts[random.randrange(0, len(potentialNexts))])
            

    return ' '.join(curWords)
    
                

print(f'Num words:\n{getTotalNumberOfWords()}')
print()
print(f'Num unique:\n{getTotalUniqueWords()}')
print()
print(f'20 Most Frequent:\n{get20MostFrequentWords()}')
print()
print(f'20 Most Frequent & Interesting:\n{get20MostInterestingFrequentWords()}')
print()
print(f'20 Least Frequent:\n{get20LeastFrequentWords()}')
print()
print(f'Frequency of "yahoos" by chapter:\n{getFrequencyOfWord("yahoos")}')
print()
# print(f'"The author gives some account of himself and family.":\nChapter {getChapterQuoteAppears("The author gives some account of himself and family.")}')
# print()
# print(f'"My father had a small estate in Nottinghamshire:"\nChapter {getChapterQuoteAppears("My father had a small estate in Nottinghamshire:")}')
# print()
# print('''"When this shower of arrows was over, I fell a groaning
# with grief and pain; and then striving again to get loose, they
# discharged another volley larger than the first, and some of them
# attempted with spears to stick me in the sides;"''')
# print(f'Chapter {getChapterQuoteAppears("When this shower of arrows was over, I fell a groaning with grief and pain; and then striving again to get loose, they discharged another volley larger than the first, and some of them attempted with spears to stick me in the sides;")}')
# print()
# print('"The people had notice, by proclamation, of my design to visit the town."')
# print(f'Chapter {getChapterQuoteAppears("The people had notice, by proclamation, of my design to visit the town.")}')
# print()
print('''"For although few men will avow their
desires of being immortal, upon such hard conditions, yet in the two
kingdoms before mentioned, of Balnibarbi and Japan, he observed that
every man desired to put off death some time longer, let it approach ever
so late: and he rarely heard of any man who died willingly, except he
were incited by the extremity of grief or torture."''')
print(f'Chapter {getChapterQuoteAppears("For although few men will avow their desires of being immortal, upon such hard conditions, yet in the two kingdoms before mentioned, of Balnibarbi and Japan, he observed that every man desired to put off death some time longer, let it approach ever so late: and he rarely heard of any man who died willingly, except he were incited by the extremity of grief or torture.")}')
print()
# print('"Yeet"')
# print(f'Chapter {getChapterQuoteAppears("yeet")}')
# print()
print(f'A random sentence:\n{generateSentence()}')


file.close()

