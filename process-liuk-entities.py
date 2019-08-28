#!/usr/bin/env python
# encoding: utf-8

import sys
import csv
from ast import literal_eval

def checkScore(value):
    if 0 <= value <= 1:
        return True
    sys.exit("Invalid score, please specify a number between 0 and 1 e.g. 0.855")

# Given a list of words, return a dictionary of
# word-frequency pairs.
# Source: https://programminghistorian.org/en/lessons/counting-frequencies
def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))

# Sort a dictionary of word-frequency pairs in
# order of descending frequency.
# Source: https://programminghistorian.org/en/lessons/counting-frequencies
def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

def main():
    common_words = ['UK', 'UKCitizenshipSupport.com', 'UKCitizenshipsupport.com', 'Page', 
    'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5', 
    'United Kingdom', 'British', 'HMSO', 'www.parliament.uk']

    if len(sys.argv) == 3:
        filename = sys.argv[1]
        min_score = float(sys.argv[2])
        checkScore(min_score)
        textlist = []

        print('Opening %s' % filename)
        lineList = [line.rstrip('\n') for line in open(filename, "r")]
        print(len(lineList))
        # Remove last list item, since it's an errorcode from Comprehend.
        lineList.pop(-1)
        with open('liuk-entities.csv', 'w+') as csvfile:
            writer = csv.writer(csvfile)
            #Header row
            writer.writerow(['Text','Type','Score','File','Line Number'])
            for line in lineList:
                try:
                    line_dict = literal_eval(line)
                    f = line_dict["File"]
                    line_number = line_dict["Line"]
                    for entity in line_dict["Entities"]:
                        score = entity["Score"]
                        if float(score) <= min_score:
                            break
                        text = entity["Text"]
                        if text in common_words:
                            break
                        # Create a list of texts, so that we can count the frequency
                        textlist.append(text)
                        t = entity["Type"]
                        writer.writerow([text,t,score,f,line_number])
                except KeyError:
                    continue
        csvfile.close()
        print("Writing entities to file.")
        dictionary = wordListToFreqDict(textlist)
        sorteddict = sortFreqDict(dictionary)
        with open('liuk-entities-freqpairs.csv', 'w+') as csvfile2:
            writer = csv.writer(csvfile2)
            #Header row
            writer.writerow(['Frequency', 'Text'])
            for row in sorteddict:
                writer.writerow(row)
        csvfile2.close()
    else:
        sys.exit("Invalid number of arguments, please run with 'python process-liuk-entities.py <filename> <score>' \
            where score is a floating point number between 0 and 1 e.g. 0.855")


if __name__ == '__main__':
    main()