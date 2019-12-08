# -*- coding: utf-8 -*-
#######################################
## COMP211 @ TUC                     ##
## Grigoriades Ioannis: 2014030007   ##
## Manesis Athanasios : 2014030061   ##
## LAB21142503                       ##
## Python Project using python3      ##
## to run under python2 change input ##
## to row_input                      ##
#######################################

##################################################################
#                      Book Layout                               #
#                                                                #
#   Book [ { afm,                                                #
#            [ {product_name, quantity, price, total_price}],    #              The book is constructed of a list of dictionaries. Each dictionary contains
#            ...                                                 #              three fields. The first one is the afm field the last one is the total field and
#            [ {product_name, quantity, price, total_price}],    #              the second field is constructed by a list of dictionaries. Each dectionary has four
#            total                                               #              fields -> product_name, quantity, price, total_price
#           }                                                    #
#            ...                                                 #
#          { afm,                                                #
#            [ {product_name, quantity, price, total_price}],    #
#            ...                                                 #
#            [ {product_name, quantity, price, total_price}],    #
#            total                                               #
#           }                                                    #
#        ]                                                       #
##################################################################

#The time is used to calculate the execution time of each option
#It is for debugging purposes and to view the times the VERBOSE mode must be
#True. The mode can be changed in main() function
import time

#Round a float up to 2 digits
#Arguments: value
#Return:    rounded value
def round_to_float(value):
    return float(round(value, 2))

#Check if the input can translate to float
#Arguments: value
#Return:    boole
def is_float(value):
    new_val = 0.00
    try:
        new_val = float(value)
    except:
        return False
    return isinstance(new_val, float)

#Check if the input can translate to integer
#Arguments: value
#Return:    boole
def is_int(value):
    new_val = 0
    try:
        new_val = int(value)
    except:
        return False
    return isinstance(new_val, int)

#Check if the given number is in the given range
#Arguments: low: The lower-end of the range, high: The higher-end of the range,
#num: The number to be compared
#Return:    0 if succeed (inside the range), 1 if failed (outside the range)
def check_int_range(low, high, num):
    if low <= num <= high:
        return 0
    else:
        return 1

#Checks if a line contains specific character
#Arguments  line: string of characters, match_of: the character contition
#Return True if it does, False if it don't
#The last character of each line is the \n (new line). So it is removed.
def match_in_line(match_of,line):
    for character in line[:-1]:
        if character != match_of:
            return False
    return True

#Check if the file exist and if it does open it
#Arguments name: The name of the file. You can provide the full path to the file
#Return     fp: The file pointer
def is_exist(name, verbose):
    try:
        fp = open(name, "r", encoding='utf-8')
    except FileNotFoundError:
        if verbose:
            print("File not found!")
        return 1
    return fp

#Check each receipt for validity
#Arguments  receipt: list [AFM:..... SYNOLO:] counter: debugging
#Return     0 if it's valid, 1 if it's not
def validate_receipt(receipt, line_counter, file_name, verbose):
    if len(receipt) < 3:
        if verbose:
            print("BUG 0: lenght error: File name: {} On line: {}".format(file_name, line_counter))
        return 1
    check_first_line = receipt[0].split()                                                                                                   #check_first_line[0] = AFM:, check_first_line[1] = AFM_NUMBER(integer)
    check_last_line = receipt[-1].split()                                                                                                   #check_last_line[0] = SYNOLO:, check_last_line[0] = SYNOLIKI_TIMI(float)
    if ( len(check_last_line) != 2 ) or ( len(check_first_line) != 2 ):                                                                     #First and last lines must have two fields
        if verbose:
            print("BUG 1: first-last not 2 fields error: File name: {} On line: {}".format(file_name, line_counter))
        return 1
    if ( check_first_line[0] != "ΑΦΜ:" ) or ( check_last_line[0] != "ΣΥΝΟΛΟ:" ):
        if verbose:
            print("BUG 2: first - last line error: File name: {} On line: {}".format(file_name, line_counter))
        return 1
    if is_int(check_first_line[1]) == False:
        if verbose:
            print("BUG 3: afm not integer: File name: {} On line: {}".format(file_name, line_counter))
        return 1
    else:
        if len(check_first_line[1]) != 10:
            if verbose:
                print("BUG 4: afm not 10 digits: File name: {} On line: {}".format(file_name, line_counter))
            return 1
    if is_float(check_last_line[1]) == False:
        if verbose:
            print("BUG 5: synolo not float: File name: {} On line: {}".format(file_name, line_counter))
        return 1
    sum = 0
    for line in range(1,len(receipt) - 1):
        check_line = receipt[line].split(":")                                                                                               #check_line[0] = product_name, check_line[1] = quantity price total_price
        check_sub_line = check_line[1].split()                                                                                              #check_sub_line[0] = quantity, check_sub_line[1] = price, check_sub_line[2] = total_price
        if len(check_sub_line) != 3:
            if verbose:
                print("BUG 6: products have no 3 fields: File name: {} On line: {}".format(file_name, line_counter))
            return 1
        if ( is_int(check_sub_line[0]) == False ) or ( is_float(check_sub_line[1]) == False ) or ( is_float(check_sub_line[2]) == False ):
            if verbose:
                print("BUG 7: products fields not in appropriate form: File name: {} On line: {}".format(file_name, line_counter))
            return 1
        if round_to_float(int(check_sub_line[0]) * float(check_sub_line[1])) != round_to_float(float(check_sub_line[2])):                   #round_to_float fixes 13.379999999999999 != 13.38                               #the sum must be valid
            if verbose:
                print("BUG 8: product total not match: File name: {} On line: {}".format(file_name, line_counter))
            return 1
        sum+=round_to_float(float(check_sub_line[2]))
    if round_to_float(sum) != round_to_float(float(check_last_line[1])):
        if verbose:
            print("BUG 9: receipt total not match: File name: {} On line: {}".format(file_name, line_counter))
        return 1
    return 0

#Create the data  of the receipts
#Arguments  receipt: the receipt is checked to be valid before-hand
#Return receipt_struct: the  of a receipt
def fill_the_structure(receipt):
    products = []
    for line in range(1,len(receipt) - 1):
        split_line = receipt[line].split(":")
        split_sub_line = split_line[1].split()
        product = {"product_name": split_line[0], "quantity": split_sub_line[0], "price": split_sub_line[1], "total_price": split_sub_line[2]}
        products.append(product)
    first_line = receipt[0].split()
    last_line = receipt[-1].split()
    receipt_struct = {"afm": first_line[1], "product": products, "total": last_line[1]}
    return receipt_struct

#Create an unsorted list of the specific layout [afm1 quantity1 ... afmN quantityN].
#Each afm it is NOT unique in this list and its product quantity is NOT added on it.
#(e.g) the list may contain [afmX quantityX afmX quantityZ]
#Mind that multiple afms with the same number may accur in the list.
#The user's input will match the upper of the receipt's product
#Arguments: book, product_name
#Return:    tmp_list
def create_option_two_list(book, product_name):
    try:                                                                                            #Preventing some errors when the function calculate the lenght of the book to be "NONE"
        if len(book) == 0:                                                                          #instead of some integer. It also returns err(1) when the user call the option two
            return 1                                                                                #before call the read option first.
    except:
        return 1
    tmp_list = []

    for receipt in range(0, len(book)):
        total = 0
        for product in range(0, len(book[receipt].get("product"))):
            if product_name == book[receipt].get("product")[product].get("product_name").upper():
                total = float(book[receipt].get("product")[product].get("total_price"))
                tmp_list.append(book[receipt].get("afm") + " " + str(total))
    return tmp_list

#It takes the list from create_option_two_list(); it makes each afm unique
#and recalculate the quantity to match the total of each afm. The function
#sort the new list by afm (low to high) and prints.
#Arguments: list: created in create_option_two_list()
#Return:    error code
def print_option_two_list(list):
    try:                                                                                #Preventing some errors when the function calculate the lenght of the book to be "NONE"
        if list == 1:                                                                   #instead of some integer. It also returns err(1) when the user call the option two
            return 1                                                                    #before call the read option first.
    except:
        return 1
    afm = []
    total_sum = []
    for row in range(0, len(list)):                                                     #Check if the afm from list[] exist in afm[] if not append afm and quantity
        if list[row].split()[0] not in afm:
            afm.append(list[row].split()[0])
            total_sum.append(float(list[row].split()[1]))
        else:                                                                           #if af already exist in afm[] update the quantity on the apropriate position
            position = afm.index(list[row].split()[0])
            total_sum[position] = float(total_sum[position]) + float(list[row].split()[1])
    unsorted_list = []
    for x in range(0, len(afm)):
        rounded_total = round(total_sum[x], 2)
        rounded_total = "{0:.2f}".format(rounded_total)                                 #fixes the 20.0. When the float if actualy an integer
        entry = afm[x] + " " + str(rounded_total)
        unsorted_list.append(entry)
    sorted_list = sorted(unsorted_list)
    for x in range(0, len(unsorted_list)):
        print(sorted_list[x])
    return 0

#Create an unsorted list of the specific layout
#[prouct product_name ... productN product_nameN].
#Each product it is NOT unique in this list and its quantity is NOT added on it.
#(e.g) the list may contain [productX quantityX productX quantityZ]
#Multiple entries with the same product name may exist in this list.
#The reason the delimeter is added is to prevent errors with multi-word product
#names
#Arguments: book, afm
#Return:    tmp_list
def create_option_three_list(book, afm):
    try:                                                                                                                                                    #Preventing some errors when the function calculate the lenght of the book to be "NONE"
        if len(book) == 0:                                                                                                                                  #instead of some integer. It also returns err(1) when the user call the option two
            return 1                                                                                                                                        #before call the read option first.
    except:
        return 1
    tmp_list = []
    for receipt in range(0, len(book)):
        if book[receipt].get("afm") == afm:
            for product in range(0, len(book[receipt].get("product"))):
                tmp_list.append(book[receipt].get("product")[product].get("product_name") + ": " + book[receipt].get("product")[product].get("total_price"))   #Each cell of the the list has a string in form of [product_name: quantity]
    return tmp_list                                                                                                                                            #Mind the character ":". The delimeter is added to be easier to split multi-words products names from its quantity

#It takes the list from create_option_three_list(); it makes each product name
#unique and recalculate the quantity to match the total of each product. The
#function sort the new list by product name (low to high) and prints.
#Arguments: list: created in create_option_three_list()
#Return:    error code
def print_option_three_list(list):
    try:                                                                                     #Preventing some errors when the function calculate the lenght of the book to be "NONE"
        if list == 1:                                                                        #instead of some integer. It also returns err(1) when the user call the option two
            return 1                                                                         #before call the read option first.
    except:
        return 1
    product = []
    total_sum = []
    for row in range(0, len(list)):                                                          #Using delimeter ":" we split each entry to its product and quantity
        if list[row].split(":")[0] not in product:
            product.append(list[row].split(":")[0])
            total_sum.append(float(list[row].split(":")[1]))                                 #If the product name is already in the product list then
        else:                                                                                #its quantity will update kepping only one product name for each.
            position = product.index(list[row].split(":")[0])
            total_sum[position] = float(total_sum[position]) + float(list[row].split(":")[1])
    unsorted_list = []
    for x in range(0, len(product)):
        rounded_total = round(total_sum[x], 2)
        rounded_total = "{0:.2f}".format(rounded_total)                                       #fixes the 20.0. When the float if actualy an integer
        entry = product[x] + " " + str(rounded_total)
        unsorted_list.append(entry)
    sorted_list = sorted(unsorted_list)
    for x in range(0, len(unsorted_list)):
        print(sorted_list[x])
    return 0

#Askes for a file name and if exist it reads it. Checks the file for valid
#receipts and parses them into the book
#Arguments: book - the data structure
#           verbose - if true prints error messages and more
#Return    book: updated
def option_one(book, verbose):
    counter = 0                                                                              #for debugging
    to_be_checked_receipt = []
    file_name = input("Enter the file's name: ")
    fp = is_exist(file_name, verbose)                                                        #is_exist(): (0 succeed, 1 failed) if succedd fp granded the file pointer
    if fp == 1:
        return book
    mode= "off"                                                                              #A switch to prevent the program read trash before the first dashes "---"
    start_timer = time.time()
    for line in fp:
        counter+= 1                                                                          #for debugging
        if (match_in_line('-',line)) == True:                                                #match_in_line() true if the line has only dashes we don't care how many
            if validate_receipt(to_be_checked_receipt, counter, file_name, verbose) == 0:    #validate_receipt() 0 if succeed; 1 if failed
                book.append(fill_the_structure(to_be_checked_receipt))                       #fill_the_() {afm,[{product_name, quantity, price, total_price}], total}
            mode="on"                                                                        #reading mode after dashes
            to_be_checked_receipt = []                                                       #empty the list
            continue                                                                         #when the dashes are found skip them and start reading from the next line
        if mode == "on":
            to_be_checked_receipt.append(line.upper())                                       #fill the list with lines until the next round of dashes while transform the letters to capitals
    fp.close()                                                                               #When the process is closed the file is closing as well... But it is a good practice (smiley face)
    end_timer = time.time()
    if verbose:
        print("Execution time of option one: {} (sec)".format(end_timer - start_timer))
    return book

#Askes the user for the product name; change it to upper-case
#Arguments: book - the data structure
#           verbose - if true prints error messages and more
#Return:    err
def option_two(book, verbose):
    err = -1
    product_name = input("Enter the product's name: ").upper()
    start_timer = time.time()
    err = print_option_two_list(create_option_two_list(book, product_name))
    end_timer = time.time()
    if verbose:
        print("Execution time of option two: {} (sec)".format(end_timer - start_timer))
    return err

#Askes the user for the afm
#Arguments: book - the data structure
#           verbose - if true prints error messages and more
#Return:    err
def option_three(book, verbose):
    err = -1
    afm = input("Enter the afm: ")
    start_timer = time.time()
    err = print_option_three_list(create_option_three_list(book, afm))
    end_timer = time.time()
    if verbose:
        print("Execution time of option two: {} (sec)".format(end_timer - start_timer))
    return err

#Just exit!
def option_four():
    exit()

#Prints on the terminal the menu and reads the user's option after ensures the
#input validity
#Arguments: verbose - if true prints error messages and more
#Return:    The option (1 - 4)
def main_menu(verbose):
    option = 0
    while True:
        try:
            option = int(input("Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program): "))
        except ValueError:
            if verbose:
                print("Enter number between 1 - 4")
            continue
        if  check_int_range(1,4,option) == 0:
            return option
        else:
            if verbose:
                print("Enter number between 1 - 4")

#The main function
def main():
    BOOK = []
    VERBOSE = False
    while True:
        option = main_menu(VERBOSE)

        if option == 1:
            BOOK = option_one(BOOK, VERBOSE)
            if VERBOSE:
                if len(BOOK) == 0:
                    print("Option one error!")
        if option == 2:
            err = option_two(BOOK, VERBOSE)
            if VERBOSE:
                if err == 1:
                    print("Option two error!")
        if option == 3:
            err = option_three(BOOK, VERBOSE)
            if VERBOSE:
                if err == 1:
                    print("Option three error!")
        if option == 4:
            option_four()

#it makes the python file a module that can be imported by another one
if __name__ == "__main__":
    main()
