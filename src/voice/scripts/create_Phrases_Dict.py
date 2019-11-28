#! /usr/bin/env python

phrases = {}
FILENAME = 'aaas.txt'

backToNewlines = open(FILENAME, 'r').read()



backToNewlines = backToNewlines.replace('\n', ' ')
backToNewlines = backToNewlines.replace("?",".")
backToNewlines = backToNewlines.replace("!",".")
sentences = backToNewlines.split(".")
sentences = [line.lstrip().rstrip() for line in sentences]
# phrases.update{'junk': 1,'kill': 2}

print(sentences)
# print(phrases)

