from tabulate import tabulate
import math

def main() : 
    test_file = input("Enter filename of test file: ")
    # open file
    f = open(test_file, "r")
    #raed lines
    test = f.readlines()
    f.close()
    #split each row per comma and convert each to float
    test = [[float(y) for y in x.split(",")]  for x in test]
    #header
    # header = ["no. of pregnancies", "glucose value", "blood pressure", "skin thickness", "insulin value", "bmi", "diabetes pedigree function", "age", "outcome"]
    # print(tabulate(test, headers=header))
    # print(type(test[0][0]))

    # read input file 
    input_file = input("Enter filename of input file: ")
    f = open(input_file, "r")
    #read lines
    input_lines = f.readlines()
    f.close()
    input_lines = [[float(y) for y in x.split(",")]  for x in input_lines]
    # print(tabulate(input_lines, headers=header[:-1]))

    # compute for distance
    neighbors_distance = [] #empty list for distance to each neighbor
    neighbors_class = [] #empty list for class of each neighbor
    # list elements may not necessarily follow the rows of the test file
    # list will be arrange according to lowest distance to highest
    # will not keep track of what exact row the nearest distance is
    # just the class of that row

    # loop for going through each row in the input file 
    k_value = int(input("Enter K-value: "))
    for i in input_lines:
        #loop for going through each row in the test file
        for j in test:
            distance = 0
            # loop through each element of each row (the columns)
            for k in range(0,len(j[:-1])):
                temp = (i[k]-j[k])**2
                distance = distance + temp
            #check if list is empty
            distance = math.sqrt(distance)
            if neighbors_distance: 
                #loop through the neighbors distance
                #lowest distance should be at neighbors_distance[0]
                for l in range(0,len(neighbors_distance)):
                    #if reached the last element just append
                    if l == len(neighbors_distance)-1 and neighbors_distance[l]<distance:
                        neighbors_distance.append(distance)
                        neighbors_class.append(j[-1])
                        break
                    elif  distance<neighbors_distance[l]:
                        if l==0:
                            neighbors_distance = [distance] + neighbors_distance
                            neighbors_class = [j[-1]] + neighbors_class
                            break
                        else:
                            neighbors_distance = neighbors_distance[0:l] + [distance] + neighbors_distance[l:]
                            neighbors_class = neighbors_class[0:l] + [j[-1]] + neighbors_class[l:]
                            break
            else : 
                neighbors_distance.append(distance)
                neighbors_class.append(j[-1])
        # print(tabulate(zip(neighbors_distance, neighbors_class), headers=["distance"]))
        # print(len(neighbors_distance))
        # print(len(neighbors_class))
        nearest_distance = neighbors_distance[0:k_value]
        neighbors_class = neighbors_class[0:k_value]
        #get the highest class occurence among nearest neighbors
        # https://stackoverflow.com/questions/6987285/find-the-item-with-maximum-occurrences-in-a-list
        class_label = max(neighbors_class,key=neighbors_class.count)
        # add that to input
        i.append(int(class_label))
        # add input to test file after labeling - as said by sir jamlech in the presentation
        test.append(i);
        #clear distance and class
        neighbors_distance = []
        neighbors_class = []
    # print(tabulate(input_lines, headers=header))
    print(tabulate(input_lines))
    # convert each row to a string with each column delimited by a comma
    #https://bobbyhadz.com/blog/python-convert-list-of-integers-to-comma-separated-string
    input_lines = [','.join([(str(j)) for j in i]) for i in input_lines]
    # join each row to a single string delimited by a newline
    input_lines = "\n".join(input_lines)
    # open file
    o = open("output.txt", "w")
    o.write(input_lines)
    o.close()
    print("Check output.txt")


 




if __name__ == '__main__':
    main()