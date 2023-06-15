import string #has a list of punctuations
import re
import decimal
from decimal import *
from tabulate import tabulate

def main():
    #open file , filename is input.txt
    f = open("input.txt", "r")
    # read each line
    file = f.readlines()
    f.close()
    # loop through each line in the file
    # 1st line is learning rate, that is index 0
    # use Decimal to be more precise
    learning_rate = Decimal(re.sub('\n','',file[0]))
    print(learning_rate)
    #get threshold at 2nd line
    threshold = Decimal(re.sub('\n','',file[1]))
    print(threshold)
    #get bias at 3rd line 
    bias = Decimal(re.sub('\n','',file[2]))
    print(bias)
    
    # start reading the feature vector
    # create an array of array to hold the feature vector ( a 2d array)
    feature_vector = []
    # start at index 3 because index 0-2 are for r, t and b 
    # the rest is the feature vector
    for i in range(3, len(file)):
        # remove trailing newline
        line = re.sub('\n','',file[i])
        # split each digit in the line and convert it to Decimal
        line = [ Decimal(y) for y in line.split()]
        feature_vector.append(line)

    #create iteration array to hold each iteration
    iteration = []
    # add each row of the vector to the iteration
    x_b_total = len(feature_vector[0]) # this is the total number of x's and b initially read from the input 
    for j in feature_vector:
        # detach z first
        z = j[len(j)-1]
        j.pop()
        # add the bias
        j.append(bias)
        # add -1 as placeholder for the weights, a, y and z in each row
        # number of -1 is equal to number values read from the input + 2 for a and y
        for k in range(0, (len(j) + 2) ):
            j.append(Decimal(-1))
        # return z to j
        j.append(Decimal(z))
        # add the row to the iteration
        iteration.append(j)
    # change initial weights of the 1st row of the vector

    # start doing the iterations for step 2
    weight = [0]*x_b_total
    tracker = 1
    output_file = open("output.txt", "w")
    while True:
        converge = True
        for l in range(x_b_total, x_b_total*2):
            iteration[0][l] = Decimal(weight[l-x_b_total])
        print("\nIteration " + str(tracker) + ':')
        output_file.write("Iteration " + str(tracker) + ':\n')
        for n in range(0, len(iteration)):
            # get a
            a = 0
            for m in range(0,x_b_total):
                a = a + (iteration[n][m]*iteration[n][m+x_b_total])
            iteration[n][x_b_total*2] = a;
            #get y 
            y = 1 if a>=threshold else 0
            iteration[n][x_b_total*2+1] = Decimal(y)
            #adjust weights
            for o in range(0,x_b_total):
                if n!= len(iteration)-1:
                    iteration[n+1][x_b_total+o] = iteration[n][x_b_total+o] + (learning_rate*iteration[n][o]*(iteration[n][-1]-y))
                else:
                    weight[o] = iteration[n][x_b_total+o] + (learning_rate* iteration[n][o]*(iteration[n][-1]-y))
            #check if converged
            # loop for each weight (column)
        print(*iteration, sep = '\n')
        print(weight)
        for p in range(x_b_total,x_b_total*2):
            # loop through each row in the column 
            comp = -1
            #compare each row
            for q in range(1, len(iteration)):
                if q == 1:
                    comp = iteration[q][p]
                else:
                    if comp != iteration[q][p]:
                        converge = False
            #compare to additional weights 
            if weight[p-x_b_total] != comp:
                converge = False
            print(converge)
        header = []
        for a in range(0,x_b_total-1):
            header.append("x"+ str(a))
        header.append("xb")
        for b in range(0,x_b_total-1):
            header.append("w"+ str(b))
        header.append("wb")
        header.append("a")
        header.append("y")
        header.append("z")
        output_file.write(tabulate(iteration, headers=header))
        output_file.write('\n')
        tracker +=1
        if converge == True:
            break
    output_file.close()


if __name__ == '__main__':
    main()

