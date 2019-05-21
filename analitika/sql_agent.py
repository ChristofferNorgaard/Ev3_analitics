import analitics as an
import sqlite3 as sql
import datetime

class sql_data:
    def __init__(self, data_loc, db_name):
        self.file_location = data_loc
        self.db_name = db_name
        try:
            self.con = sql.connect(self.file_location)
        except:
            raise ValueError('Invalid file name, connection did not procede')
    def convert_to_sql(id, html_string, gyro_object):
        string_to_format = "INSERT INTO {0} VALUES ({1},{2},{3},{4});" #id, time, ride_data_array, html

    def create_db(self):
        command = "CREATE TABLE {0}(id INTEGER PRIMARY KEY, date TEXT, was_completed INTEGER, gyro TEXT, html TEXT)".format(self.db_name)
        self.con.execute(command)
        
def import_ride(sql_data_class, csv_file, date = datetime.datetime.now()):
    rides = an.process_csv(csv_file)
    was_complete = {False : 0, True : 1}
    for ride in rides:
        was_complite_bit = was_complete[ride.wasEnded]
        date_string = str(date)
        gyro_object = an.Gyro(ride)
        gyro_text = str(gyro_object.convert_to_string())
        html_text = an.graph(gyro_object)
        execute_text = 'INSERT INTO {0}(date, was_completed, gyro, html) VALUES (?,?,?,?)'.format(sql_data_class.db_name)
        sql_data_class.con.execute(execute_text, (date_string, was_complite_bit, gyro_text, html_text))

def printRide(sql_data_class, command):
    cur = sql_data_class.con.cursor()
    cur.execute(command)
    return cur.fetchall()
