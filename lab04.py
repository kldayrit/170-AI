import string #has a list of punctuations
import re
from tabulate import tabulate

def main():
    #ask user for file name
    filename = input("Enter file name: ")
    #open file
    f = open(filename, "r")
    file = f.read()
    f.close()
    #split files with spaces
    words = file.split()
    #clean words and also convert them to lower case
    for i in range(len(words)):
        # if a character of the word matches with any punctuation remove it
        # matches non alphanumeric characters in a word using regex and replace them with empty character ''
        words[i] = re.sub(r'[^a-zA-Z0-9]', '', words[i])
        words[i] = words[i].lower()
    #create list bag to hold words and frequency to list frequency
    bag = []
    frequency = []
    total = len(words)
    for j in range(len(words)):
        # if word is already in the bag increment its value by 1
        match = 0
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
    # i zip yung words at frequency then sort according sa words
    data = sorted(zip(bag,frequency))
    # magigign tuple siya kasi zinip so kunin mo yung first sa tuple para sa word then 2nd para sa frequency
    bag = [x[0] for x in data]
    frequency = [y[1] for y in data]
    index = list(range(len(bag)))
    table = zip(index,bag, frequency)
    headers = ['Index', 'Word', 'Frequency']
    dict_size = 'Dictionary Size: ' + str(size)
    total_num = 'Total Number of Words: ' + str(total)
    print(dict_size)
    print(total_num)
    print(tabulate(table, headers=headers))
    o = open("output.txt", "w")
    o.write(dict_size)
    o.write('\n' + total_num)
    for l in range(len(bag)):
        o.write('\n' + bag[l] + ' '+  str(frequency[l]))
    o.close()





if __name__ == '__main__':
    main()