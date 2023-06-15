import re
import tabulate
import copy


def readfile():
    filename = "hmm.in"
    f = open(filename, "r")
    file = f.read()
    file = file.split('\n')
    f.close()
    return file

def markov(file):
    # read strings considered
    no_of_strings = int(file[0]) + 1

    # put all strings in a list
    strings_considered = []
    for i in range(1,no_of_strings):
        strings_considered.append(file[i])

    #possible values for each state
    states = file[no_of_strings].split(' ')
    #possible obserable measurement values for each state
    obv_val = file[no_of_strings+1].split(' ')

    value_index = no_of_strings+2
    #get the probability for the pair values
    # they will be in the form ['ES', 0.1] where ES would be P(E|S) and 0.1 is its probability
    pair_values = {}
    for j in range(0,len(states)):
        pair = [ float(i)  for i in file[value_index].split(' ')]
        for k in range(0,len(obv_val)):
            pair_values[ obv_val[k]+states[j]]= pair[k]
        value_index +=1

    # get the cases
    # they will be in the form ['S', 'E', 1] where S is the state, E is the measurement value, 1 would be the index 
    no_of_cases = int(file[value_index])
    value_index+=1
    cases = [file[value_index+i]  for i in range(0,no_of_cases)]
    copy_cases = copy.deepcopy(cases)
    cases = [re.sub(' given ',' ', i)   for i in cases]
    cases = [i.split(' ')  for i in cases]
    for i in cases:
        i.append(int(i[0][-1]))
        i[0] = i[0][:-1]
        i[1] = i[1][:-1]

    #computation 
    #get transition probabilities
    o = open("hmm.out", "w")
    for i in strings_considered: #loop through the strings
        o.write(i + '\n')
        # get count of states
        count = {}
        for j in states:
            count[j] = i[:-1].count(j) # don't count last since it does not have a next state

        #transiton probability
        trans_prob = {}
        for k in states:
            for l in states:
                # https://stackoverflow.com/questions/2970520/string-count-with-overlapping-occurrences
                regex = "(?=" + k+l + ")"
                trans_prob[l+k] =len(re.findall(regex ,i)) / count[k]

        # get probability of each state, S0, S1, S2 , T0, T1, T2and so on
        state_prob= {}
        if states[0] == i[0]:
            state_prob[states[0]] = [1]
            state_prob[states[1]] = [0]
        else:
            state_prob[states[0]] = [0]
            state_prob[states[1]] = [1]
        
        #loop iterations = length of string
        for y in range(1, len(i)):
            current_state = 0
            # probability of S1 , T1 and so on
            for z in states:
                sta = states[0]+z
                curr = trans_prob[sta] * state_prob[z][y-1]
                current_state+=curr
            state_prob[states[0]].append(current_state)
            state_prob[states[1]].append(1-current_state)

        #compute the cases
        count =0
        for x in cases:
            case_pair = x[1] + x[0]
            numerator = pair_values[case_pair] * state_prob[x[0]][x[2]]
            denominator = 0
            # probability of E0 or F0 
            for a in states:
                sta = x[1] + a
                curr = pair_values[sta] * state_prob[a][x[2]]
                denominator+=curr
            answer = round(numerator/denominator,4)
            o.write(copy_cases[count] + ' = ' + str(answer) + '\n')
            count+=1
    o.close()
        




def main():
    file = readfile()
    markov(file)


if __name__ == '__main__':
    main()