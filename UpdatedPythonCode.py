import mysql.connector
from mysql.connector import errorcode



def attribute_display(input_table, cur):
    instr = ("select * from", input_table)
    cur.execute(instr)
    print("The attributes that you can view from this table are:\n")
    for i in range(len(cur.column_names)):  
        print((cur.column_names)[i]," ")
    print("Please input below the attributes you would like to view from this table:\n")
    input3 = input()
    if input3 not in cur.column_names:
        print("Please input attributes that belong to the table like the one's listed above:\n")
        attribute_display(input_table)
    for i in input3:
        cur.execute("select", i, "from", input_table)
        print("Here are all the records for that attribute(s) you wanted to view:\n")
        print(cur.fetchall())
    return

def row_display(input_table,cur):
    row_count = 0
    cur.execute("select * from",input_table)
    whole = cur.fetchall()
    for row in whole:
        row_count += 1
    print("How many rows would you like to display? \n")
    row_input1 = int(input())
    if row_input1 > row_count:
        print("Sorry, but thats an invalid input as not that many rows exist in that table\n")
        print("Please enter the number of rows you would like displayed:\n")
        row_input2 = int(input())
        if row_input2 > row_count:
            print("invalid input")
            exit()
    if row_input1 == row_count:
        print(whole)
    if row_input1 < row_count:
        print("Which rows specifically would you like to see?\n")
        print("Please input the row numbers starting from 1 up to the max row number seperated by whitespace of which you would like to see\n")
        row_input3 = input()
        empty_list = []
        for i in row_input3:
            empty_list.append(i)
        for i in empty_list:
            if i > row_count:
                print("At least one invalid input is present\n")
                exit()
        if len(empty_list) > row_count:
            print("You entered more rows than is present in the table\n")
            exit()
        for i in empty_list:
            cur.execute("select row_number(empty_list[i]) over(len(empty_list)) as num_row FROM", input_table)
            print(cur.fetchall())
    return


def value_display(input_table, cur):
    return


# Below function will handle printing/ querying entire tables.
def query(input_table, cur):
    if input_table == '' or None:
        table_selection = input("Which table would you like to query? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
        while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
            print("Invalid selection\n")
            table_selection = input("Which table would you like to query? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
        input_table = table_selection
        cur.execute("select * from", input_table)
    print("Would you like to view the entire table (Y/N) ?:\n")
    user_input = input()
    if user_input == 'Y':
        cur.execute("select * from",input_table)
        print(cur.fetchall())
    elif user_input == 'N':
        print("Options:\n")
        print("1- Display Certain Attributes (columns)")
        print("2- Display Certain Rows of the Table")
        print("3- Display Certain Values of Table")
        user_input = int(input())
        if user_input == 1:
            attribute_display(input_table)
        elif user_input == 2:
            row_display(input_table)
        elif user_input == 3:
            value_display(input_table)

    #Left off here 
    # dope. maybe copy the code and paste into github, if not I can.
    # I'll do that now
    #attribute_selection = input("Which attribute would you like to query? (Enter the attribute name or * to select all attributes):\n")
    
    #while(attribute_selection not in cur.column_names and attribute_selection != "*"):
    #    print("Invalid selection\n")
   #     attribute_selection = input("Which attribute would you like to query? (Enter the attribute name or * to select all attributes):\n")
    #if attribute_selection == "*":
   #     print(cur.fetchall())
   # else:
   #     cur.execute("select", attribute_selection, "from", table_selection)


def admin_consol():
    pass
        
def data_entry(cur, cnx):
    menu = "What would you like to do:\n1 - Perform a query\n2 - Insert new tuples to a table using a file\n3 - Insert new tuples to a table using prompts\n4 - Update a tuple\n5 - Delete a tuple\n6 - Exit"
    selection = int(input(menu))
    while (selection > 6 or selection < 1):
        print("Invalid selection\n")
        selection = int(input(menu))
    if selection == 1:
        query(None)
    elif selection == 2:
        pass   
    elif selection == 3:
        pass
    elif selection == 4:
        update_tuple(cur)
    elif selection == 5:    
        delete_tuple(cur, cnx)
    elif selection == 6:
        return

def update_tuple(cur, cnx):
    print("Which table would you like to update? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    table_selection = input()
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to update? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
    
    print("Which attribute would you like to update? (Enter the attribute name):\n")
    update_attribute_selection = input()
    cur.execute("select * from", table_selection)
    while (update_attribute_selection not in cur.column_names):
        print("Invalid selection\n")
        update_attribute_selection = input("Which attribute would you like to update? (Enter the attribute name):\n")
    
    update_value_selection = input("What would you like to update the value to?\n")
    
    condition_attribute_selection = input("Which attribute would you like to use as a condition? (Press enter to have no condition[updates every {} value in {} to {}]):\n".format(update_attribute_selection, table_selection, update_value_selection))
    while (condition_attribute_selection not in cur.column_names and condition_attribute_selection != ""):
        print("Invalid selection\n")
        condition_attribute_selection = input("Which attribute would you like to use as a condition? (Press enter to have no condition[updates every {} value in {} to {}]):\n".format(update_attribute_selection, table_selection, update_value_selection))
    
    if condition_attribute_selection == "":
        cur.execute("update", table_selection, "set", update_attribute_selection, "=", update_value_selection)
    
    else:
        condition_value_selection = input("What would you like the condition value to be?\n")
        cur.execute("update", table_selection, "set", update_attribute_selection, "=", update_value_selection, "where", condition_attribute_selection, "=", condition_value_selection)
    
    cnx.commit()
    if cur.rowcount == 0:
        print("No tuples were updated")
    else:
        print("Updated {} tuples".format(cur.rowcount)) 

def delete_tuple(cur, cnx):
    print('Which table would you like to delete a tuple from? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n')
    table_selection = input()
    while (table_selection != "ARTIST" and table_selection != "EXHIBITION" and table_selection != "ART_OBJECT" and table_selection != "PERMANENT_COLLECTION" and table_selection != "OTHER_COLLECTION" and table_selection != "BORROWED_COLLECTION" and table_selection != "OTHER" and table_selection != "PAINTING" and table_selection != "STATUE"):
        print("Invalid selection\n")
        table_selection = input("Which table would you like to query? (ARTIST, EXHIBITION, ART_OBJECT, PERMANENT_COLLECTION, OTHER_COLLECTION, BORROWED_COLLECTION, OTHER, PAINTING, STATUE):\n")
   
    print('Which attribute would you like to use to delete a tuple? (or press enter to delete all contents of table):\n')
    attribute_selection = input()
    cur.execute("select * from", table_selection)
    while (attribute_selection not in cur.column_names and attribute_selection != ""):
        print("Invalid selection\n")
        attribute_selection = input("Which attribute would you like to use to delete a tuple? (or press enter to delete all contents of table):\n")
    
    if attribute_selection == "":
        cur.execute("delete from", table_selection)
    
    else:
        print('Enter a value condition to use to delete a tuple(s):\n')
        value_selection = input()
        cur.execute("delete from", table_selection, "where", attribute_selection, "=", value_selection)
    
    cnx.commit()
    if(cur.rowcount == 0):
        print("No tuples were deleted\n")
    else:
        print(cur.rowcount, "record(s) deleted")

def guest_view():
    print("What are you looking for:\n")
    print("1- Artist Information\n")
    print("2- Exhibit Information\n")
    print("3- Art Object information\n")
    print("4- Permanent collection of Art Objects\n")
    print("5- Borrowed Collection of Art Objects\n")
    print("6- Other Collection of Art Objects\n")
    print("7- Painting Information\n")
    print("8- Statue Information\n")
    print("9- Other Types of Art\n")
    print("Please input a number corresponding to a table that you would like to view:\n")
    # From here, depending on what the user inputs they will then be prompted if they want to see a specific
    # attribute from the table or if they want to execute a particular join to merely see attributes belonging to two seperate tables.
    table = ''
    selection = int(input())
    if selection not in range(1, 10):
        guest_view()
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
    
    if table != '' or None:
        query(table)
                
                

            
    
    '''
    if selection == '2':
        subselection = input('Please type 1 for Athletes or 2 for Coaches:\n')
        if subselection == '1':
            athlete_info(cur)
    '''


def athlete_info(cur):
    '''
    instr=""
    join=""
    
    att_selection = input("Do you want to see the Athlete name ? Y or N: ")
    if att_selection == 'Y':
        join = 'from athlete naturaljoin PARTICIPANT'
    

    #instr="select * from athlete where olympicid = %(oid)s"
    instr="select * from athlete"
    searchkey=input("please insert the olympicid of the athlete you are looking for (press Enter to view all):") or None

    #cur.execute(instr,{'oid':searchkey})
    cur.execute(instr)
    col_names=cur.column_names
    search_result=cur.fetchall()
    print("Search found ",len(search_result)," Entries:\n")
    header_size=len(col_names)
    for i in range(header_size):
        print("{:<15s}".format(col_names[i]),end='')
    print()
    print(15*header_size*'-')
    for row in search_result:
        for val in row:
            print("{:<15s}".format(str(val)),end='')
        print()
    '''


if __name__ == "__main__":
    
    # Connect to server
    print("Welcome to the Arts Museum Database:")
    print("In order to proceed please select your role from the list below:\n")
    print("1-DB Admin")
    print("2-Data Entry")
    print("3-Browse as guest")

    selection = int(input())

    if selection in ['1','2']:
        username= input("user name:")
        passcode= input("password:")
    else:
        username="guest"   
        passcode=None
    
    try:
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=33060,
            user=username,
            password=passcode)    
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Issue with username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


            
    # Get a cursor
    cur = cnx.cursor()

    fd = open('DBNAME.SQL', 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cur.execute(command)
        except IOError:
            print("unable to open")
    

    # Execute a query
    cur.execute("use Art_museum")
    if selection == '1':
        admin_consol()
    elif selection == '2':
        data_entry()
    else:
        guest_view()
    #insert example
    inst_country_template= "insert into country values (%s,%s,%s,%s)"

    countryname= input("Please insert name of country to add: ")
    gnum = input("How many gold medals do this country have (press enter and leave blank if unknown): ") or None
    snum = input("How many silver medals do this country have (press enter and leave blank if unknown): ") or None
    bnum = input("How many bronze medals do this country have (press enter and leave blank if unknown): ") or None

    print(type(gnum))
    print(type(snum))

    inst_country_data = (countryname,gnum,snum,bnum)
    cur.execute(inst_country_template,inst_country_data)
    cnx.commit()

     # Close connection
    
    cnx.close()


