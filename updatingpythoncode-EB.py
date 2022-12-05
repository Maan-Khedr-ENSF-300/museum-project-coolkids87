import mysql.connector
from mysql.connector import errorcode
import os

# revised attribute_display... seems to check out.

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

def row_display(input_table, cur, cnx):
    cursor = cnx.cursor(buffered=True)
    row_count = 0
    cursor.execute("SELECT * FROM {}".format(input_table))
    at_names = cursor.column_names
    whole = cursor.fetchall()
    row_count = len(whole)
    print("How many rows would you like to display? \n")
    row_input1 = int(input())
    if row_input1 > row_count:
        print("Sorry, but thats an invalid input as not that many rows exist in that table\n")
        print("Please enter the number of rows you would like displayed:\n")
        row_input2 = int(input())
        if row_input2 > row_count:
            print("Invalid input. Goodbye")
            exit()
    # everything up to here is good.
    
    if row_input1 == int(row_count):
        size  = len(whole)
        for i in range(size):
            for x in range(len(whole[i])):
                print(f'{whole[i][x]: <20}', end = ' ')
            print()

    # everything up to here is good.
    
    if row_input1 < int(row_count):
        print("Which rows specifically would you like to see?\n")
        print("Please input the row numbers starting from 1 up to the max row number seperated by whitespace of which you would like to see\n")
        row_input3 = (input())
        print(row_input3)
        empty_list = []
        for i in row_input3:
            empty_list.append(i)
        
        '''
        row_str = ''
        counter = 0
        for i in empty_list:
            if counter < len(empty_list) -1:
                row_str += i + ', '
            else:
                row_str += i
            counter += 1
        print(row_str)
        '''

        # below loop checks over 
        '''
        for i in row_input3:
            if (i > row_count or i < 0):
                print("At least one invalid input is present\n")
                exit()
            count += 1
        '''

        # below loop checks if user inputted more rows than is in the table
        if len(empty_list) > row_count:
            print("You entered more rows than is present in the table\n")
            exit()

        if row_input3 == None:
            print("You dont want to see any rows\n")
            return

        cursor.execute("SELECT * FROM {}".format(input_table))
        rows = cursor.fetchall()
        size = len(rows)
        for i in range(size):
            if i == (j for j in empty_list):
                for x in range(len(rows[i])):
                    print(f'{rows[i][x]}:35', end = ' ')
                print()
    return


def value_display(input_table, cur):
    """
    Input:
        The table that the user wants to view the values.
        The cursor object.

    Output:
        Displays all the values of that table.
    
    Features:
        Displays all the values that the user can view from the table.
        If the user inputs a value that does not belong to the table, the program will ask the user to input a value that does belong to the table.
    """
    instr = ("select * from", input_table)
    cur.execute(instr)
    print("The values that you can view from this table are:\n")
    for i in range(len(cur.column_names)):  
        print((cur.column_names)[i]," ")
    print("Please input below the values you would like to view from this table:\n")
    input3 = input()
    if input3 not in cur.column_names:
        print("Please input values that belong to the table like the one's listed above:\n")
        value_display(input_table)
    for i in input3:
        cur.execute("select", i, "from", input_table)
        print("Here are all the records for that value(s) you wanted to view:\n")
        print(cur.fetchall())
    return


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
            row_display(input_table,cur,cnx)
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
    menu = "What would you like to do:\n1 - Perform a query\n2 - Insert new tuples to a table using a file\n3 - Insert a tuple to a table using prompts\n4 - Update a tuple\n5 - Delete a tuple\n6 - Exit\n"
    selection = int(input(menu))
    while (selection > 6 or selection < 1):
        print("Invalid selection\n")
        selection = int(input(menu))
    if selection == 1:
        query(None, cur)
    elif selection == 2:
        insert_tuple_file(cur, cnx)   
    elif selection == 3:
        insert_tuple_prompt(cur)
    elif selection == 4:
        update_tuple(cur, cnx)
    elif selection == 5:    
        delete_tuple(cur, cnx)
    elif selection == 6:
        return
    
def insert_tuple_file(cur, cnx):
    table_selection = input("Which table would you like to insert a tuple into? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to insert a tuple into? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    
    filename = input("Please enter the name of the file you would like to open(each line of text in the file should be attribute values corresponding to the order in the table, separated by commas):\n")
    insert_file = open(filename, "r")
    for line in insert_file.readlines():
        cur.execute("insert into", table_selection, "values", line)
        cnx.commit()
    insert_file.close()


def insert_tuple_prompt(cur):
    table_selection = input("Which table would you like to insert a tuple into? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to insert a tuple into? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    cur.execute("select * from", table_selection)
    
    attribute_list = []
    for col_name in cur.column_names:
        attribute_selection = input("Enter the value for " + col_name + ":\n")
        attribute_list.append(attribute_selection)
    
    
    cur.execute("insert into", table_selection, "values", attribute_list)

    cur.commit()

    

def update_tuple(cur, cnx):
    print("Which table would you like to update? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    table_selection = input()
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to update? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    
    print("Which attribute would you like to update? (Enter the attribute name):\n")
    update_attribute_selection = input()
    cur.execute("select * from {}".format(table_selection))
    while (update_attribute_selection not in cur.column_names):
        print("Invalid selection\n")
        update_attribute_selection = input("Which attribute would you like to update? (Enter the attribute name):\n")
    
    update_value_selection = input("What would you like to update the value to?\n")
    
    condition_attribute_selection = input("Which attribute would you like to use as a condition? (Press enter to have no condition[updates every {} value in {} to {}]):\n".format(update_attribute_selection, table_selection, update_value_selection))
    while (condition_attribute_selection not in cur.column_names and condition_attribute_selection != ""):
        print("Invalid selection\n")
        condition_attribute_selection = input("Which attribute would you like to use as a condition? (Press enter to have no condition[updates every {} value in {} to {}]):\n".format(update_attribute_selection, table_selection, update_value_selection))
    
    if condition_attribute_selection == "":
        cur.execute("update {} set {} = {}".format(table_selection, update_attribute_selection, update_value_selection))
    
    else:
        condition_value_selection = input("What would you like the condition value to be?\n")
        cur.execute("update {} set {} = {} where {} = {}".format(table_selection, update_attribute_selection, update_value_selection, condition_attribute_selection, condition_value_selection))
    
    cnx.commit()
    if cur.rowcount == 0:
        print("No tuples were updated")
    else:
        print("Updated {} tuples".format(cur.rowcount)) 

def delete_tuple(cur, cnx):
    cursor = cnx.cursor(buffered=True)
    print('Which table would you like to delete a tuple from? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n')
    table_selection = input()
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to query? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    #good
    print('Which attribute would you like to use to delete a tuple? (or press enter to delete all contents of table):\n')
    attribute_selection = input()
    cursor.execute("SELECT * FROM {}".format(table_selection))
    while (attribute_selection not in cursor.column_names and attribute_selection != ""):
        print("Invalid selection\n")
        attribute_selection = input("Which attribute would you like to use to delete a tuple? (or press enter to delete all contents of table):\n")
    if attribute_selection == "":
        cursor.execute("DELETE FROM {}".format(table_selection))
    else:
        print('Enter a value condition to use to delete a tuple(s):\n')
        value_selection = input()
        cursor.execute("DELETE FROM {} WHERE {} = {}".format(table_selection, attribute_selection, value_selection))
    cnx.commit()
    if(cur.rowcount == 0):
        print("No tuples were deleted\n")
    else:
        print(cursor.rowcount, "record(s) deleted")

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
    fd = open("test.sql", "r")
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
