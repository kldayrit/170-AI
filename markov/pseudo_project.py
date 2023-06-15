#=================================================================================================
# RECIPE DICTIONARY
recipeDictionary = {}
# ex. dictionary input 
# { name : [ description, {itemName: itemAmount, itemName: itemAmount, ...  } ] }
# the keys in the recipe dictionary will be the name with a value list
# the list value would have the following:
# 0 index : description
# 1 index : another dictionary of ingredients , this dictionary would have:
## ingredient name as the key and ingredient amount as value (ex. {itemName: itemAmount})

#########################
# add something that will read a file to populate the recipeDictionary

# RECIPE BOOK FUNCTIONS
def addRecipe():
    global recipeDictionary
    # Ask user for recipe name

    # Ask user for recipe description

    # Ask user for number of ingredients (this is to know how many time we should ask the user for ingredients)
    
    # This wil be used to hold the ingredients inputted by the user that does not exist
    nonexistentIngredients = []
    # Loop equal to the number of ingredients
    # inside the loop ask user for each ingredient name and ingredient amount
    # Check each ingredient name per iteration if it is in supplyDictionary, if not add to nonexistendIngredients

    # Loop through the nonexistentIngredients list and call addRecordSupply for each element

    # Update the file of the recipeDictionary
    ...

def deleteRecipe():
    global recipeDictionary
    # Show all Recipe in the dictionary
    # One way to do this is to loop through the dictionary and show all the names

    # Ask user input for recipe name to delete

    # Check first if it exists
    # If it does , then delete it and show a message indicating success
    # update the file for the recipe dictionary

    # if it does not then just print something to indicate failure
    ...

def deleteAllRecipe():
    # OPTIONAL : Ask user for Y input if they really want to delete all recipe
    # if Y then just loop through each keys in the dictionary and delete them all

    # if anything other than Y then just print something to indicate invalid input
    ...

def viewRecipe():
    # Loop through all keys of the recipe dictionary and print them all

    # Ask user for input of recipe name
    
    # check if recipe name is in dictionary
    # if it is print it
    # if not print something to indicate invalid input
    ...

def executeRecipe():
    # Show all recipe names

    # Ask user for input of recipe name to execute

    #check if recipe name is in the dictionary
    # if it is show all ingredient name with their corresponding amount
    # show options: [1] Done [2] cancel
    # if Done
    # check if an each ingredient has sufficient amount in the supply dictionary
    # if not print something for error and exit function
    # if sufficient, reduce ingredient amount in supply dictionary with proper amount
    # if Cancel
    # just print something for cancel and exit the function

    ...
#=================================================================================================

#=================================================================================================
#supply dictionary
supplyDictionary = {}
# ex. dictionary input
# supplyDictionary = {name : [stock , price] }

# lagay ng magbabasa from file ng mga dictionary input

# SUPPLY RECORD FUNCTIONS
# functions will be the same as above , if natapos na yun pareho lang mga next
# just follow the parameters in the pdf file, but same logic as previous functions
def addRecordSupply():
    global supplyDictionary
    ...

def deleteRecordSupply():
    global supplyDictionary
    ...

def deleteAllRecordSupply():
    global supplyDictionary
    ...

def viewRecordSupply():
    global supplyDictionary
    ...

#=================================================================================================
# dictionary
supplierDictionary = {}
# ex. dictionary input
# supplierDictionary = {name : contact}

# SUPPLIER RECORDS FUNCTIONS
def addSupplierRecord():
    ...

def deleteSupplierRecord():
    ...

def deleteAllSupplierRecord():
    ...

def viewSupplierRecord():
    ...

#=================================================================================================
# MAIN

def main():
    while True:
        # Just edit this if you want design
        print("=============WELCOME===============\n")
        print("Select Something to Edit")
        print("[1] Recipe Book")
        print("[2] Supply Records")
        print("[3] Supplier Records")
        print("[0] EXIT")
        print("===================================\n")
        choice = int(input("Enter Choice: "))
        if choice == 0:
            break
        elif choice == 1:
            print("===================================")
            print("Select Something to do")
            print("[1] Add Recipe")
            print("[2] Delete Recipe ")
            print("[3] Delete All Recipes")
            print("[4] View Recipe")
            print("[5] Execute Recipe")
            print("[0] EXIT")
            print("===================================")
            choice = int(input("Enter Choice: "))
            if choice == 0:
                break
            elif choice == 1:
                addRecipe()
            elif choice == 2:
                deleteRecipe()
            elif choice == 3:
                deleteAllRecipe()
            elif choice == 4:
                viewRecipe()
            elif choice == 5:
                executeRecipe()
            else:
                print("Invalid Input")
        elif choice == 2:
            print("===================================")
            print("Select Something to do")
            print("[1] Add Record ")
            print("[2] Delete Record ")
            print("[3] Delete All Records ")
            print("[4] View Record ")
            print("[0] EXIT")
            print("===================================")
            choice = int(input("Enter Choice: "))
            if choice == 0:
                break
            elif choice == 1:
                addRecordSupply
            elif choice == 2:
                deleteRecordSupply
            elif choice == 3:
                deleteAllRecordSupply
            elif choice == 4:
                viewRecordSupply
            else:
                print("Invalid Input")
        elif choice == 3:
            print("===================================")
            print("Select Something to do")
            print("[1] Add Record ")
            print("[2] Delete Record ")
            print("[3] Delete All Records ")
            print("[4] View Record ")
            print("[0] EXIT")
            print("===================================")
            choice = int(input("Enter Choice: "))
            if choice == 0:
                break
            elif choice == 1:
                addSupplierRecord
            elif choice == 2:
                deleteSupplierRecord
            elif choice == 3:
                deleteAllSupplierRecord
            elif choice == 4:
                viewSupplierRecord
            else:
                print("Invalid Input")
        else:
            print("Invalid Input")





main()