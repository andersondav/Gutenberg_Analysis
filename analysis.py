#!/usr/bin/python3

import sys, string, re
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
    if c != '\'' and c != '-':
        punc.append(c)
print(punc)
punc = ''.join(punc)

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
        common_words = getCommonWords(1000)
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


file.close()

