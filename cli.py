import os
import sql_agent as sql
from beautifultable import BeautifulTable
from PyInquirer import style_from_dict, Token, prompt, Separator
import webbrowser
import analitics as an
import math
import datetime
import base64
clear = lambda: os.system('cls')
cache = [None,None,None,None,None,None,None,None,None,None,None]
clear()
print("  ______ __      __ ____              _   _            _   __     __ _______  _____  _____   _____ ")
print(" |  ____|\ \    / /|___ \      /\    | \ | |    /\    | |  \ \   / /|__   __||_   _|/ ____| / ____|")
print(" | |__    \ \  / /   __) |    /  \   |  \| |   /  \   | |   \ \_/ /    | |     | | | |     | (___  ")
print(" |  __|    \ \/ /   |__ <    / /\ \  | . ` |  / /\ \  | |    \   /     | |     | | | |      \___ \ ")
print(" | |____    \  /    ___) |  / ____ \ | |\  | / ____ \ | |____ | |      | |    _| |_| |____  ____) |")
print(" |______|    \/    |____/  /_/    \_\|_| \_|/_/    \_\|______||_|      |_|   |_____|\_____||_____/ ")
print("For more go to https://github.com/ChristofferNorgaard/Ev3_analitics")
#creating script
try:
    sql_ag = sql.sql_data("database.db", "database")
    print("Database connection is operational")
    version = 0
except:
    print("Make sure that you runned setup. Exiting program.")
    input("Press any key to continue...")
    raise SystemExit
#cui -functions
def set_new_version(new_version):
    version = new_version

filter_dict = {
        "mission" : "mission == '{0}'",
        "date_higher" : "date >= Convert(TIMESTAMP, {0})",
        "date_lower" : "date <= Convert(TIMESTAMP, {0})",
        "was completed" : "was_completed == 1",
        "version_higher" : "version > {0}",
        "version_lower" : "version < {0}"
    }

def filter_print_from_data():
    command = "SELECT id, date, mission, was_completed, version FROM database" + filter_database()
    a = sql.printRide(sql_ag, command)
    table = BeautifulTable()
    for row in reversed(a):
        table.append_row(row)

    print(table)

def filter_database():
    style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
    })
    filters_questions = [    
    {
        'type': 'confirm',
        'message': 'Select successful runs?',
        'name': 'was_completed',
        'default': True,
    },
    {
        'type': 'list',
        'name': 'missions',
        'message': "What mission do you need",
        'choices': ['V01', 'V02', 'V03', 'V04', 'V05', "Don't use mission filter"],
    },
    
    {
        'type': 'input',
        'name': 'version',
        'message': "write version in format version#(higher or lower), write whatever not to us date filter",
        'default' : '0#higher'
    },
    
    ]
    filters = prompt(filters_questions, style=style) #{'exit': True, 'missions': 'V05', 'date': ''} example
    print(filters)
    command_array = []
    if (filters['was_completed'] == True):
        command_array.append(filter_dict['was completed'])
    if (filters['missions'] is not "Don't use mission filter"):
        command_array.append(filter_dict['mission'].format(filters['missions']))
    try:
        versions = filter['version'].split('#')
        if versions[0] == 'higher':
            command_array.append(filter_dict['version_higher'].format(int(versions[0])))
        elif versions[1] == 'lower':
            command_array.append(filter_dict['version_lower'].format(int(versions[0])))
        else:
            raise ValueError('wrong value')
    except:
        pass
    command = ''
    if len(command_array) == 1:
        command = " WHERE " + command_array[0]
    elif len(command_array) > 1:
        command = " WHERE "
        for commands in command_array[:-1]:
            command += commands + " AND "
        command += command_array[-1]
    
    return command
def SaveMenu(element = None, select_from_menu = False):
    print("Where would you like to save this element?")
    for i in range(0, 10):
        if cache[i] == None:
            print("{0} .place = Not used".format(str(i)))
        else: 
            print("{0} .place = {1}".format(str(i), str(cache[i])[0:48]))
    print("Write number where you would like to save (or load) from your element or write anything not number to cancel")
    a = input(":: ")
    try:
        selected_place = int(a)
    except:
        print("save canceled")
        return None
    if select_from_menu:
        return cache[selected_place]
        print("loaded successfully")
    else:
        cache[selected_place] = element
        print("saved successfully")
def GetXanY(element):
    if  type(element) is list:
        return element[1], element[2]
    else:
        return element.x_ar, element.y_ar
def show(html):
    myFile = open("new.html", "w+")
    myFile.write(html)
    webbrowser.open_new("new.html")
    print("html opened")
#mainloop
while True:
    print("(i)Import, (p)show database data, (h)help, (c)clear (e)exit, (v)version, (m)math_and_graph")
    user_input = input(":: ")
    if "h" in user_input:
        print("(i)Import will import csv file in database. A file location will be requested in follow-up")
        print("(e)Export will export database for later use. Database imports are not yet completed")
        print("(p)show database data will allow you to interact with database")
        print("(e)exit will exit the app")
        print("(c)clear will clear the cmd")
        print("(v)version will change the current version for importing file")
        print("(m) will allow you to calculate and show graphs")
        print("write function that you desiree in input marked by ::")
        continue
    elif user_input == "c":
        clear()
        continue
    elif user_input == "i":
        fill_loc = input("write file location of csv file:: ")
        #try:
        sql.import_ride(sql_ag,fill_loc,version)
        print("File imported, you can check it if you want.")
        #except Exception as e:
            #print(e)
            #print("Invalid filename")
            #continue
    elif user_input == "e":
        print("Exiting program")
        input("Press any key to continue...")
        raise SystemExit
    elif user_input == "v":
        us_input = input("Write new version...")
        try:
            us_input = int(us_input)
        except:
            print("This is not correct number")
            continue
        version = us_input
        print("Now the version is {0}".format(str(version)))
    elif user_input == "p":
        go_back = True
        while go_back:
            print("(s)show whole database, (sf)show whole database whit filters, (sl)select, (h)help, (c)clear, (e)exit from this function, (c)show cache")
            user_input = input(":: ")
            if 'h' in user_input:
                print("(s) will show whole database non-filtered")
                print("(sf) will show whole database filtered")
                print("(sl) will allow you to select based on id")
                print("(c) will clear the screen")
                print("(e) will exit from this function and will go back to first menu")
                print("(c) will show cache, a place where you save things")
            elif "s" == user_input:
                a = sql.printRide(sql_ag, "SELECT id, date, mission, was_completed, version FROM database")
                table = BeautifulTable()
                for row in a:
                    table.append_row(row)
                print(table)
            elif "sf" == user_input:
                command = "SELECT id, date, mission, was_completed, version FROM database" + filter_database()
                a = sql.printRide(sql_ag, command)
                table = BeautifulTable()
                for row in reversed(a):
                    table.append_row(row)
                print(table)
            elif "sl" == user_input:
                #try:
                    selection_id = int(input("Write selected id:: "))
                    command = "SELECT * FROM database WHERE ID == {0}".format(str(selection_id))
                    a = sql.printRide(sql_ag, command)
                    if len(a) == 0:
                        print("ID not in database")
                    else:
                        print("This is your selected element:")
                        print(str(a)[0:52])
                        SaveMenu(a)
                #except:
                    #print("Input not number")
            elif "e" == user_input:
                go_back = False
            elif "c" == user_input:
                for i in range(0, 10):
                    if cache[i] == None:
                        print("{0} .place = Not used".format(str(i)))
                    else: 
                        print("{0} .place = ".format(str(i)) + str(cache[i])[0:60])
        
    elif "m" == user_input:
        print("(s) to show graph, (a) to calculate average, (d) to calculate_div, (sl) for advance graphs, (h)help")
        us_input = input(":: ")
        if "h" in us_input:
            print("(s) will allow you to show your graph in browser from where you last saved it")
            print("(a) will allow you to show you to calculate average from database")
            print("(d) will allow you to calculate deviation from another ride saved in cache")
            print("(sl) will allow you to compare graphs and to show average on graphs")
        elif "s" == us_input:
            element = SaveMenu(select_from_menu=True)
            html = str(element[0][6])
            #url = "text/html;base64," + base64.encodestring(html.encode())
            show(html)
        elif "a" == us_input:
            print("select filters for avarage output")
            command = "SELECT gyro FROM database" + filter_database()
            result = sql.printRide(sql_ag, command)
            print(result[0])
            gyro_arr = []
            if len(result) == 0:
                print("There are no elements that can be found under this filter")
                continue
            for element in result:
                new_gyro_object = an.GyroObject.convert_from_string(element[0])
                gyro_arr.append(new_gyro_object)

            x, y = an.average(gyro_arr)
            element = ["average", x, y]
            SaveMenu(element)
            print("complete")
        elif "d" == us_input:
            print("Select reference from cache")
            reference = SaveMenu(select_from_menu=True)
            print("Select the element for comparison")
            selected = SaveMenu(select_from_menu=True)  
            reference_object = an.GyroObject.convert_from_string(reference[0][5])
            selected_object = an.GyroObject.convert_from_string(selected[0][5])
            deviation = an.deviation(GetXanY(selected_object), GetXanY(reference_object))
            print(deviation)
        elif "sl" == us_input:
            print("(c)compare up to 3 rides, (a) print avarage in graph")
            us_input = input(":: ")
            if us_input == "c":
                print("Select first for comparison")
                element1 = SaveMenu(select_from_menu=True)
                print("Select second for comparison")
                element2 = SaveMenu(select_from_menu=True)
                comparison_list_str = [element1, element2]
                print("Do you want another element for comparison? [y,n]")
                us_input = input(":: ")
                if us_input == "y":
                    element3 = SaveMenu(select_from_menu=True)
                    comparison_list_str.append(element3)
                comparison_list = []
                for element in comparison_list_str:
                    gyroelement = an.GyroObject.convert_from_string(element[0][5])
                    comparison_list.append(gyroelement)
                    print(gyroelement.other_data_ar)
                html = an.graph(comparison_list)
                show(html)
            else:
                print("Select average object")
                element = SaveMenu(select_from_menu=True)
                html = an.graph([], [element[1], element[2]])   
                show(html)

        else:
            print("invalid command")
    else:
        print("invalid command")