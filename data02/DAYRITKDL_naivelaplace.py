import string #has a list of punctuations
import re
import os
import numpy as np
from tabulate import tabulate
#https://www.pythontutorial.net/advanced-python/python-decimal/
#we will use this to prevent errors that may result from floating point arithmeti
import decimal
from decimal import *
#https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
from pathlib import Path


spamBOW = []
spamFREQ = []
spam_dict_size = 0
spam_total_num = 0
hamBOW = []
hamFREQ = []
ham_dict_size = 0
ham_total_num = 0
spam_size = 0
ham_size = 0

def bagOfWords(filename, bag, frequency):
    #ask user for file name
    #open file
    f = open(filename, "r", encoding='ISO-8859-1') 
    file = f.read()
    f.close()
    #split files with spaces
    words = file.split()
    #clean words and also convert them to lower case
    for i in range(len(words)):
        # if a character of the word matches with any punctuation remove it
        # matches non alphanumeric characters in a word using regex and replace them with empty character ''
        # https://datagy.io/python-remove-punctuation-from-string/#:~:text=One%20of%20the%20easiest%20ways,maketrans()%20method.
        words[i] = re.sub(r'[^a-zA-Z0-9]', '', words[i])
        words[i] = words[i].lower()
    #create list bag to hold words and frequency to list frequency
    for j in range(len(words)):
        # if word is already in the bag increment its value by 1
        match = 0
        if words[j] == "":
            continue
        for k in range(len(bag)):
            if words[j] == bag[k]:
                frequency[k] +=1
                match += 1
        # else create new key value
        if match == 0:
            bag.append(words[j])
            frequency.append(1)
        match -= 1
    size = len(bag)
    total = sum(frequency)
    # i zip yung words at frequency then sort according sa words
    data = sorted(zip(bag,frequency))
    # magigign tuple siya kasi zinip so kunin mo yung first sa tuple para sa word then 2nd para sa frequency
    sorted_bag = [x[0] for x in data]
    sorted_frequency = [y[1] for y in data]
    return size, total, sorted_bag, sorted_frequency

# this function gets the bag of words of the files in the spam directory
# we assume that the data set for spam is in the spam folder
# we assume the same for ham which we assume to be in the ham folder
def getSpamBOW(directory):
    global spamBOW, spamFREQ, spam_dict_size, spam_total_num, spam_size
    #iterate through each file in the folder
    # https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/
    for filename in os.scandir(directory):
        spam_size += 1
        if filename.is_file():
            spam_dict_size , spam_total_num, spamBOW, spamFREQ= bagOfWords(filename.path, spamBOW, spamFREQ)

    o = open("spam_output.txt", "w")
    o.write('Dictionary Size: ' + str(spam_dict_size))
    o.write('\n'  + 'Total Number of Words: ' + str(spam_total_num))
    for l in range(len(spamBOW)):
        o.write('\n' + spamBOW[l] + ' '+  str(spamFREQ[l]))
    o.close()

# this function gets the bag of words of the files in the spam directory
# the same as getSpamBOW()
def getHamBOW(directory):
    global hamBOW, hamFREQ, ham_dict_size, ham_total_num, ham_size
    for filename in os.scandir(directory):
        ham_size += 1
        if filename.is_file():
            ham_dict_size , ham_total_num, hamBOW, hamFREQ= bagOfWords(filename.path, hamBOW, hamFREQ)

    o = open("ham_output.txt", "w")
    o.write('Dictionary Size: ' + str(ham_dict_size))
    o.write('\n'  + 'Total Number of Words: ' + str(ham_total_num))
    for l in range(len(hamBOW)):
        o.write('\n' + hamBOW[l] + ' '+  str(hamFREQ[l]))
    o.close()

def getProb(bow, freq, k):
    global hamBOW, hamFREQ, ham_dict_size, ham_total_num, spamBOW, spamFREQ, spam_dict_size, spam_total_num, spam_size, ham_size
    prob_spam = Decimal(str(spam_size + k)) / ( Decimal(str(spam_size + ham_size)) + Decimal(str(2 * k)))
    prob_ham = Decimal(str(ham_size + k)) / ( Decimal(str(spam_size + ham_size)) + Decimal(str(2 * k)))
    prob_message_spam = 1
    prob_message_ham = 1
    prob_message = 0
    prob_spam_message = 0
    # get prob_message_spam
    #get count of unique words in ham and spam
    #https://www.programiz.com/python-programming/methods/set/symmetric_difference
    #https://stackoverflow.com/questions/28444561/get-only-unique-elements-from-two-lists
    # get the symmetric difference
    unique_sd = list(set(spamBOW).symmetric_difference(set(hamBOW)))
    # also get the intersection
    unique_inters = list(set(spamBOW).intersection(set(hamBOW)))
    unique = len(unique_sd) + len(unique_inters)
    #get count of new words
    count_new = 0
    for z in range(len(bow)):
        if bow[z] in spamBOW:
                continue
        if bow[z] in hamBOW:
                continue
        count_new +=1
    for i in range(len(bow)):
        count_spam = 0
        count_ham = 0 
        if bow[i] in spamBOW:
            ind = spamBOW.index(bow[i])
            count_spam += spamFREQ[ind]
        if bow[i] in hamBOW:
            ind = hamBOW.index(bow[i])
            count_ham += hamFREQ[ind]
        prob_message_spam = Decimal(str(prob_message_spam)) * Decimal(str( (count_spam + k) / (spam_total_num  + (k * (unique + count_new)))))
        prob_message_ham = Decimal(str(prob_message_ham)) * Decimal(str( (count_ham + k) / (ham_total_num  + (k * (unique +  count_new)))))
    prob_message = Decimal(str(prob_message_spam * prob_spam)) + Decimal(str(prob_message_ham * prob_ham))
    prob_spam_message = Decimal(str(prob_message_spam * prob_spam)) /  Decimal(str(prob_message))
    return Decimal(str( prob_spam_message))


def main():
    getSpamBOW('spam')
    getHamBOW('ham')
    k = Decimal(input("Enter smoothing factor, k: "))
    directory = 'classify'
    test_BOW = []
    test_FREQ = []
    o = open("classify.out", "w")
    for filename in os.scandir(directory):
        if filename.is_file():
            test_dict_size , test_total_num, test_BOW, test_FREQ = bagOfWords(filename.path, test_BOW, test_FREQ)
            prob = getProb(test_BOW, test_FREQ, k)
            if(Decimal(prob) < Decimal(0.5)):
                print(Path(filename.path).stem + ' HAM ' + str(prob) + '\n')
                o.write(Path(filename.path).stem + ' HAM ' + str(prob) + '\n')
            else: 
                print(Path(filename.path).stem+ ' SPAM ' + str(prob) + '\n')
                o.write(Path(filename.path).stem + ' SPAM ' + str(prob) + '\n')
            test_BOW = []
            test_FREQ = []
    o.write('\nHAM\n')
    o.write('Dictionary Size: ' + str(ham_dict_size))
    o.write('\n'  + 'Total Number of Words: ' + str(ham_total_num) + '\n')
    o.write('\nSPAM\n')
    o.write('Dictionary Size: ' + str(spam_dict_size))
    o.write('\n'  + 'Total Number of Words: ' + str(spam_total_num) + '\n')
    o.close()

if __name__ == '__main__':
    main()