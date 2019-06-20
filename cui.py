import analitics as an
import datetime
import sql_agent as sql
import os
from beautifultable import BeautifulTable
from PyInquirer import style_from_dict, Token, prompt, Separator
import datetime

sql_ag = sql.sql_data('database.db','database')
try:
    sql_ag.create_db()
    version = 0
except:
    print('The database is already created.')
    version = sql_ag.con.execute("SELECT MAX(version) FROM database")

filter_dict = {
        "mission" : "mission == {0}",
        "date_higher" : "date >= Convert(TIMESTAMP, {0})",
        "date_lower" : "date <= Convert(TIMESTAMP, {0})",
        "was completed" : "was_completed == 1",
        "version_higher" : "version > {0}",
        "version_lower" : "version < {0}"
    }
def set_new_version(new_version):
    version = new_version
    
def printfromdata(argstring):
    if argstring == "FILTER":
        command = "SELECT id, date, mission, was_completed, version FROM database" + filter_database()
    else:
        command = "SELECT id, date, mission, was_completed FROM database"
    a = sql.printRide(sql_ag, command)
    table = BeautifulTable()
    for row in reversed(a):
        table.append_row(row)

    print(table)

clear = lambda: os.system('cls')

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
        'name': 'date',
        'message': "write date in format DD-MM-YYYY#(higher or lower), write whatever not to us date filter",
        'default' : '01-01-2019#higher'
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
    date = filters['date'].split('#')
    try:
        date_format = '%d-%m-%Y'
        date_obj = datetime.datetime.strptime(date[0], date_format)
        if date[1] == 'higher':
            command_array.append(filter_dict['date_higher'].format(datetime.datetime.timestamp(date_obj)))
        elif date[1] == 'lower':
            command_array.append(filter_dict['date_lower'].format(datetime.datetime.timestamp(date_obj)))
        else:
            raise ValueError('wrong value')
    except:
        pass
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
        


filter_database()