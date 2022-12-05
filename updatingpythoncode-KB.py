import mysql.connector
from mysql.connector import errorcode
import os

#revised and tested insert_tuple_prompt function -- looks good
#revised and tested insert_tuple_file function -- looks good (attached the txt file I used to test it)
#revised update_tuple function -- I was unable to test it due to issues on my end, if someone could test it that would be great
#revised delete_tuple function -- I was unable to test it due to issues on my end, if someone could test it that would be great

def attribute_display(input_table, cur, cnx):
    cursor = cnx.cursor(buffered=True)
    instr = ("select * from {}".format(input_table))
    cursor.execute(instr)
    print("The attributes that you can view from this table are:\n")
    for i in range(len(cursor.column_names)):  
        print((cursor.column_names)[i],end = ' ')                    # displays every column/attribute in the table the user inputted
    print("Please input below the attributes you would like to view from this table:\n")
    input3 = input()
    user_inlist = input3.split()
    list_length = len(user_inlist)
    sstring = ''
    counter = 0
    for i in user_inlist:
        if counter < list_length - 1:
            sstring += i + ', '
        else:
            sstring += i + ' '
        counter += 1
    cursor.execute("SELECT {} FROM {}".format(sstring, input_table))
    print("Here are all the records for that attribute(s) you wanted to view:\n")
    for i in user_inlist:
        print(f'{i:45}', end = ' ')
    print('-' * 40 * len(user_inlist))
    all_recs = cursor.fetchall()
    num_rows = len(all_recs)                # gets the number of rows/records
    for j in range(num_rows):                      
        for k in range(len(all_recs[j])):
            print(f'{all_recs[j][k]:45}', end = ' ')
        print()
    return

def row_display(input_table,cur):
    row_count = 0
    cur.execute("select * from {}".format(input_table))
    whole = cur.fetchall()
    for row in whole:
        row_count += 1
    print("How many rows would you like to display? \n")
    row_input1 = int(input())
    if row_input1 > int(row_count):
        print("Sorry, but thats an invalid input as not that many rows exist in that table\n")
        print("Please enter the number of rows you would like displayed:\n")
        row_input2 = int(input())
        if row_input2 > row_count:
            print("invalid input")
            exit()
    if row_input1 == int(row_count):
        size  = len(whole)
        for i in range(size):
            for x in range(len(whole[i])):
                print(f'{whole[i][x]: <20}')
            print()
    if row_input1 < int(row_count):
        print("Which rows specifically would you like to see?\n")
        print("Please input the row numbers starting from 1 up to the max row number seperated by whitespace of which you would like to see\n")
        row_input3 = input()
        empty_list = []
        for i in row_input3:
            empty_list.append(i)
        count = 0
        for i in empty_list:
            if count > row_count:
                print("At least one invalid input is present\n")
                exit()
            count += 1
        if len(empty_list) > row_count:
            print("You entered more rows than is present in the table\n")
            exit()
        if row_input3 == None:
            print("You dont want to see any rows\n")
            return
        
        for i in empty_list:
            cur.execute("select row_number() over() AS num_row, ArtID, Type, Style FROM {}".format(input_table))
            print(cur.fetchall(), end = '\n')
    return


def value_display(input_table, cur):
    pass


# Below function will handle printing/ querying entire tables for non-admin users.

def query(input_table, cur, cnx):
    if input_table == None:
        table_selection = input("Which table would you like to query? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
        while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
            print("Invalid selection\n")
            table_selection = input("Which table would you like to query? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
        input_table = table_selection
    print("Would you like to view the entire table (Y/N) ?: ")
    user_input = input()
    print()
    if user_input == 'Y':
        cur.execute('SELECT * FROM {}'.format(input_table))     # bug fix: for all selct from statements in execute we must use .format
        at_names = cur.column_names
        print("Result:\n")
        for i in range(len(at_names)):
            print(f'{at_names[i]:40}', end = ' ')
        print()
        rows = cur.fetchall()
        print(( (len(at_names)) * 40 ) * '-' )
        size  = len(rows)
        for i in range(size):
            for x in range(len(rows[i])):
                if rows[i][x] == None:
                    print('')
                else:
                    print(f'{rows[i][x]:40}', end = ' ')
            print()
    if user_input == 'N':
        print("Options:\n")
        print("1- Display Certain Attributes (columns)")
        print("2- Display Certain Rows of the Table")
        print("3- Display Certain Values of Table")
        user_input = int(input())
        if user_input == 1:
            attribute_display(input_table, cur, cnx)
        elif user_input == 2:
            row_display(input_table,cur)
        elif user_input == 3:
            value_display(input_table)


def admin_consol(cur, cnx):
    print('Select an option:\n1 - Perform a query\n2 - Provide the path and file name of an sql script file to the application, which will then run the script file on MySQL using the connector\n3 - exit')
    user_input = int(input())
    if user_input not in [1, 2, 3]:
        print("Invalid input\n")
        user_input = int(input())
    
    if user_input == 1:
        command = input("Type your SQL command here:\n")
        if ('INSERT' in command) or ('UPDATE' in command) or ('DELETE' in command):
            cur.execute(command)
            cnx.commit()
        else:
            cur.execute(command)
            rows = cur.fetchall()
            at_names = cur.column_names
            print("Result:\n")
            for i in range(len(at_names)):
                print(f'{at_names[i]:20}', end = ' ')
            print()
            print((len(rows[0]) * 20) * '-')
            size = len(rows)
            for i in range(size):
                for x in range(len(rows[i])):
                    if rows[i][x] == None:
                        print('')
                    else:
                        print(f'{rows[i][x]:20}', end = ' ')
                print('\n')
            
      
    if user_input == 2:                                         # connects the admin to the .sql script of their choice.
        print("Please provide the file pathway below:\n")
        path_input = input()
        if os.path.exists(path_input) == 1:                     # Boolean verification to ensure the file pathway inputted by the user exists.
            cur.execute("source",path_input)
        else:
            print("Please print a file pathway that exists on your computer:\n")
            path_input = input()
            cur.execute("source",path_input)

    if user_input == 3:                                    # lets the user exit the application.
        print("goodbye\n")
        exit()
        


        
def data_entry(cur, cnx):
    menu = "\nWhat would you like to do:\n1 - Perform a query\n2 - Insert new tuples to a table using a file\n3 - Insert a tuple to a table using prompts\n4 - Update a tuple\n5 - Delete a tuple\n6 - Exit\n"
    selection = int(input(menu))
    while (selection > 6 or selection < 1):
        print("Invalid selection\n")
        selection = int(input(menu))
    if selection == 1:
        query(None, cur, cnx)
    elif selection == 2:
        insert_tuple_file(cur, cnx)   
    elif selection == 3:
        insert_tuple_prompt(cur, cnx)
    elif selection == 4:
        update_tuple(cur, cnx)
    elif selection == 5:    
        delete_tuple(cur, cnx)
    elif selection == 6:
        exit(1)
    
def insert_tuple_file(cur, cnx):
    table_selection = input("Which table would you like to insert a tuple into? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to insert a tuple into? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    cur.execute("SELECT * FROM {}".format(table_selection))
    alist = list(cur.column_names)

    cur.fetchall()

    filename = input("Please enter the name of the file you would like to open(each line of text in the file should be attribute values corresponding to the order in the table, separated by commas):\n")
    insert_file = open(filename, "r")
    while (insert_file == None):
        print("Invalid file name\n")
        filename = input("Please enter the name of the file you would like to open(each line of text in the file should be attribute values corresponding to the order in the table, separated by commas):\n")
        insert_file = open(filename, "r")
    alist = [line.rstrip() for line in insert_file]
    for line in alist:
        try:
            cur.execute("INSERT INTO {} VALUES {}".format(table_selection, line))
            cnx.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            data_entry(cur, cnx)
        cnx.commit()
    insert_file.close()
    print("\nInsertion successful\n")
    data_entry(cur, cnx)


def insert_tuple_prompt(cur, cnx):
    table_selection = input("Which table would you like to insert a tuple into? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to insert a tuple into? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    cur.execute("select * from {}".format(table_selection))
    
    attribute_list = []
    for col_name in cur.column_names:
        attribute_selection = input("Enter the value for " + col_name + ":\n")
        attribute_list.append(attribute_selection)
    attribute_tuple = tuple(attribute_list)
    cur.fetchall()
    
    try:
        cur.execute("INSERT INTO {} VALUES {}".format(table_selection, attribute_tuple))
        print("\nTuple inserted successfully\n")
        cnx.commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        data_entry(cur, cnx)

    data_entry(cur, cnx)

    

def update_tuple(cur, cnx):
    table_selection = input("Which table would you like to update? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to update? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    
    cur.execute("select * from {}".format(table_selection))
    update_attribute_selection = input("Which attribute would you like to update from {}? (Enter the attribute name):\n".format(cur.column_names))

    while (update_attribute_selection not in cur.column_names):
        print("Invalid selection\n")
        update_attribute_selection = input("Which attribute would you like to update from {}? (Enter the attribute name):\n".format(cur.column_names))
    
    update_value_selection = input("What would you like to update the {} value to?\n".format(update_attribute_selection))
    
    condition_attribute_selection = input("Which attribute would you like to use as a condition from {}? (Enter the attribute name)\n(Press enter to have no condition[updates every {} value in {} to {}]):\n".format(cur.column_names, update_attribute_selection, table_selection, update_value_selection))
    while (condition_attribute_selection not in cur.column_names and condition_attribute_selection != ""):
        print("Invalid selection\n")
        condition_attribute_selection = input("Which attribute would you like to use as a condition from {}? (Enter the attribute name)\n(Press enter to have no condition[updates every {} value in {} to {}]):\n".format(cur.column_names, update_attribute_selection, table_selection, update_value_selection))
    
    cur.fetchall()
    try:
        if condition_attribute_selection == "":
            cur.execute("UPDATE {} SET {} = {}".format(table_selection, update_attribute_selection, update_value_selection))
    
        else:
            condition_value_selection = input("What would you like the condition value to be?\n")
            print()
            cur.execute("UPDATE {} SET {} = {} WHERE {} = {}".format(table_selection, update_attribute_selection, update_value_selection, condition_attribute_selection, condition_value_selection))

        if cur.rowcount == 0:
            print("No tuples were updated")
        else:
            print("Updated {} tuples".format(cur.rowcount)) 
        cnx.commit()
        data_entry(cur, cnx)

    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        data_entry(cur, cnx)


def delete_tuple(cur, cnx):
    table_selection = input('Which table would you like to delete a tuple from? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n')
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to query? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    #good
    cur.execute("select * from {}".format(table_selection))

    attribute_selection = input('Which attribute would you like to use to delete a tuple from {}?\n(or press enter to delete all contents of table):\n'.format(cur.column_names))
    while (attribute_selection not in cur.column_names and attribute_selection != ""):
        print("Invalid selection\n")
        attribute_selection = input('Which attribute would you like to use to delete a tuple from {}?\n(or press enter to delete all contents of table):\n'.format(cur.column_names))
    
    cur.fetchall()
    if attribute_selection == "":
        try:
            cur.execute("DELETE FROM {}".format(table_selection))
            print("Deleted {} tuples".format(cur.rowcount))
            cnx.commit()
            data_entry(cur, cnx)
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            data_entry(cur, cnx)
    else:
        value_selection = input('Enter a value condition to use to delete a tuple(s):\n')
        try:
            cur.execute("DELETE FROM {} WHERE {} = {}".format(table_selection, attribute_selection, value_selection))
            print("Deleted {} tuples".format(cur.rowcount))
            cnx.commit()
            data_entry(cur, cnx)
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            data_entry(cur, cnx)

def guest_view(cur, cnx):
    print("What are you looking for:\n")
    print("1- Artist Information")
    print("2- Exhibit Information")
    print("3- Art Object information")
    print("4- Permanent collection of Art Objects")
    print("5- Borrowed Collection of Art Objects")
    print("6- Other Collection of Art Objects")
    print("7- Painting Information")
    print("8- Statue Information")
    print("9- Other Types of Art")
    print("Please input a number corresponding to a table that you would like to view: ")
    # From here, depending on what the user inputs they will then be prompted if they want to see a specific
    # attribute from the table or if they want to execute a particular join to merely see attributes belonging to two seperate tables.
    table = ''
    selection = int(input())
    if selection not in range(1, 10):
        guest_view()
    else:
        if selection == 1:
            table = 'ARTIST'
        elif selection == 2:
            table = 'EXHIBITION'
        elif selection == 3:
            table = 'ART_OBJECT'
        elif selection == 4:
            table = 'PERMANENT_COLLECTION'
        elif selection == 5:
            table = 'OTHER_COLLECTION'
        elif selection == 6:
            table = 'BORROWED_COLLECTION'
        elif selection == 7:
            table = 'PAINTING'
        elif selection == 8:
            table = 'STATUE'
        elif selection == 9:
            table = 'OTHER'
        
    if table != '' or table != None:
        query(table, cur, cnx)
        
def main():   
    # Connect to server
    print("Welcome to the Arts Museum Database:")
    print("In order to proceed please select your role from the list below:\n")
    print("1-DB Admin")
    print("2-Data Entry")
    print("3-Browse as guest")

    selection = int(input())
    while selection not in [1,2,3]:
        print("Invalid selection")
        selection = int(input())

    if selection in [1,2]:
        username= input("user name:")
        passcode= input("password:")
    else:
        username="guest"   
        passcode=None
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user=username,
        password=passcode,
        auth_plugin = 'mysql_native_password')  
    cur = cnx.cursor()
    fd = open("DB.sql", "r")
    sqlfile = fd.read()
    fd.close()
    sqlcommands = sqlfile.split(';')
    for command in sqlcommands:
        try:
            if command.strip() != '':
                cur.execute(command)
        except(IOError):
            print("command skipped")
    # Get a cursor
    # Execute a query
    cur.execute("use Art_museum")
    if selection == 1:
        admin_consol(cur, cnx)
    elif selection == 2:
        data_entry(cur, cnx)
    else:
        guest_view(cur, cnx)

     # Close connection
    cnx.close()

if __name__ == "__main__":
    main()
