from tabulate import tabulate
import math
import random
import re
from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as st
import matplotlib.pyplot as plt

def readFile(filename, dictionary):
    #read values from file
    f = open(filename, "r")
    file = f.readlines()
    f.close()
    #get header from first line of file
    headers = file[0].split(',')
    headers[-1] = re.sub(r'\s','',headers[-1])# remove trailing new character from last header
    file = file[1:] # remove headers
    no_of_columns = len(headers)
    columns = [[] for y in range(no_of_columns)] # initialize list of list for each column
    #traverse the file
    for i in range(0,len(file)):
        #get the line and split it to each column
        line = file[i].split(',')
        line[-1] = re.sub(r'\s','',line[-1])
        line = [float(x) for x in line]
        file[i] = line
        # add each value of the line to their column
        for j in range(0, no_of_columns):
            columns[j].append(line[j])
    #create dictionary 
    # the header is the key and the value is its column
    for k in range(0,no_of_columns):
        dictionary[headers[k]]= columns[k]
    temp = zip(*columns)
    return dictionary, temp, headers,file
    # print(tabulate(temp,headers=headers))

def getCluster(clusternum, table_values, headers, table_rows, choice1, choice2, text_area, root):
    #clear text area
    plt.clf()
    text_area.delete(1.0,END)
    if choice1 == choice2:
        plt.close()
        error = "Attribute 1 and Attribute 2 should not be the same"
        text_area.insert(tk.INSERT,error)
        return error
    # get random rows equivalent to number of clusters as centrois
    centroid= [[table_rows[random.randint(0,len(table_rows)-1)][choice1] ,table_rows[random.randint(0,len(table_rows)-1)][choice2] ]for y in range(clusternum)]
    
    # test file to check output
    # centroid = [[11.76, 2.68], [13.77, 1.9]]
    
    #get nearest points to each centroid
    count = 0 
    while(True):
        cluster = [[] for x in range(clusternum)] 
        true_cluster = [[[],[]] for x in range(clusternum)] 
        for i in range(0,len(table_rows)):
            # skip if centroid is equal to current row
            if i in centroid:
                continue
            #since we only get 2 columns we just do squareroot of ( x0 - c0  )^2 + ( x1 - c1  )^2 where 0 and 1 is choice1 and choice2 respectively
            distance = []
            # get distance for each centroid
            for j in centroid:
                temp_distance = math.sqrt( ((table_rows[i][choice1] - j[0])**2) + ((table_rows[i][choice2]-j[1])**2) )
                distance.append(temp_distance)
            # get the nearer centroid
            nearest = distance.index(min(distance))
            cluster[nearest].append(i)
            # print(str(distance) +' '+ str(nearest))

        # create new centroids 
        # new centroid 0
            
        # write output to output.csv
        # output will be a string containing the centroids and the points near it
        output = ""
        for z in range(0,clusternum):
            output = output + 'Cluster ' + str(z) + ': (' + str(centroid[z][0]) + ' , ' + str(centroid[z][1]) + ')\n'
            for y in cluster[z]:
                # create a new true cluster list that will hold the exact values of each point
                true_cluster[z][0].append(table_rows[y][choice1])
                true_cluster[z][1].append(table_rows[y][choice2])
                output = output + "[" + str(table_rows[y][choice1]) + ' , ' + str(table_rows[y][choice2]) + "]\n"
            output = output + "\n"
        o = open("output.csv", "w")
        o.write(output)
        o.close()
        new_centroid = [[] for x in range(clusternum)] 
        count+=1
        for k in range(0,clusternum):
            if len(cluster[k]) == 0:
                new_centroid[k]= centroid[k]
                continue
            x_value = 0
            y_value = 0
            for l in cluster[k]:
                x_value = x_value + table_rows[l][choice1]
                y_value = y_value + table_rows[l][choice2]
            new_centroid[k].append(x_value/len(cluster[k]))
            new_centroid[k].append(y_value/len(cluster[k]))
        same = True
        for m in range(0,clusternum):
            if new_centroid[m][0] != centroid[m][0] or new_centroid[m][1] != centroid[m][1]:
                same = False
        if same == True:
            break
        else: 
            for o in range(0,clusternum):
                centroid[o] = new_centroid[o]
    text_area.insert(tk.INSERT,output)
    #https://coderslegacy.com/python/python-matplotlib/python-matplotlib-scatter-plot/
    for a in range(0,clusternum):
        plt.scatter(true_cluster[a][0],true_cluster[a][1])
    plt.title('K means scatter plot')
    plt.xlabel(headers[choice1])
    plt.ylabel(headers[choice2])
    plt.show()
    return output
    

def resetAll(choice1, choice2, clusternum, headers, text_area):
    plt.close()
    text_area.delete(1.0,END)
    choice1.set(headers[0])
    choice2.set(headers[1])
    clusternum.set(2)

def main():
    table_values = {}
    filename = "Wine.csv"
    #get table values from file
    table_values, zipped_columns, headers, table_rows = readFile(filename, table_values)

    #temp value for testing
    # clusternum = 2 #number of clusters
    # choice1 = 0   # first column values
    # choice2 = 1   # 2nd column values
    # out = getCluster(clusternum, table_values, headers, table_rows, choice1, choice2)

    # gui 
    root = Tk()
    root.title("K means clustering")

    # drop down menus for attribute selection
    # https://www.geeksforgeeks.org/dropdown-menus-tkinter/
    root.geometry("700x600")
    root.configure(bg="lightgray")
    label1 = tk.Label(root, text='Select Atrribute 1 :')
    label1.place(x=5,y=5)
    choice1= StringVar()
    choice1.set(headers[0])
    drop1 = OptionMenu(root, choice1,*headers)
    drop1.pack()
    drop1.place(x=115,y=0)

    label2 = tk.Label(root, text='Select Atrribute 2 :')
    label2.place(x=5,y=35)
    choice2= StringVar()
    choice2.set(headers[1])
    drop2 = OptionMenu(root, choice2,*headers)
    drop2.pack()
    drop2.place(x=115, y=30)

    # for number of clusters
    label3 = tk.Label(root, text='Enter N clusters :')
    label3.place(x=5,y=65)
    number = range(1,11)
    clusternum= IntVar()
    clusternum.set(number[1])
    drop3 = OptionMenu(root, clusternum,*number)
    drop3.pack()
    drop3.place(x=115, y=60)

    # text area for the output (centroids and cluster) 
    # https://www.geeksforgeeks.org/python-tkinter-scrolledtext-widget/
    label4 = tk.Label(root, text='Centroids & Clusters')
    label4.place(x=20,y=300)
    output_area = st.ScrolledText(root,
                            width = 55, 
                            height = 28 )
    output_area.grid(column = 0, pady = 10, padx = 10)
    output_area.pack()
    output_area.place(x=150,y=120)

    # button to run the function
    # why lambda =https://stackoverflow.com/questions/32056064/python-tkinter-button-to-run-function-with-multiple-arguments-not-working
    run = tk.Button(root, text="RUN", command=lambda: getCluster(clusternum.get(), table_values, headers, table_rows, headers.index(choice1.get()), headers.index(choice2.get()),output_area,root))
    run.pack()
    run.place(x=35,y=90)
    
    reset = tk.Button(root, text="RESET", command=lambda: resetAll(choice1,choice2,clusternum,headers, output_area))
    reset.pack()
    reset.place(x=85,y=90)
    
    root.mainloop()
    


if __name__ == '__main__':
    main()