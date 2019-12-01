#! /usr/bin/env python


def phrase_Create():

    FILENAME = 'aaas.txt'

    backToNewlines = open(FILENAME, 'r').read()


    backToNewlines = backToNewlines.replace('\n', ' ')
    backToNewlines = backToNewlines.replace("?",".")
    backToNewlines = backToNewlines.replace("!",".")
    sentences = backToNewlines.split(".")
    sentences = [line.lstrip().rstrip() for line in sentences]

    keyCount = 0
    keyList = []

    for each in sentences:
        keyList.append(keyCount)
        keyCount = keyCount + 1

    phrases = dict(zip(keyList,sentences))
    return phrases
    # print(phrases)

