#imports
import csv
import json
import math
from bokeh.plotting import figure, output_file, show, ColumnDataSource
import bokeh as bk
import time
from bokeh.embed import file_html
from bokeh.resources import Resources
#class definitions
class DataNode:
    def __init__(self, time, dataArray=[], com=None, reset=[],):
        self.time = time
        self.dataArray = dataArray # [GIRO;ROTATIONS_B;ROTATIONS_C;SPEED_B;SPEED_C;COLOR_3;COLOR_1]
        self.com = com
        self.reset = reset
    
    def encode(self):
        return {"time":self.time, "dataArray":self.dataArray, "com":self.com, "reset":self.reset}
    
    def decode(dict):
        return DataNode(dict["time"], dict["dataArray"], dict["com"], dict["reset"])

class RideData:
    def __init__(self, ride_number, dataArray, wasEnded):
        self.ride_number = ride_number
        self.dataArray = dataArray
        self.wasEnded = wasEnded

class GyroObject:
    def __init__(self, text, y_ar, x_ar, other_data_ar, ride_num, was_ended):
        #text, y_ar, x_ar, other_data_ar, ride_num, was_ended
        self.text = text
        self.y_ar = y_ar 
        self.x_ar = x_ar
        self.other_data_ar = other_data_ar
        self.ride_num = ride_num
        self.was_ended = was_ended
        


    def convert_to_string(self):
        other_data = '-'.join(str(x) for x in self.other_data_ar)
        string_list = [self.text, '_'.join(str(x) for x in self.y_ar), '_'.join(str(x) for x in self.x_ar), '_'.join(other_data), str(self.ride_num), str(self.was_ended)]
        return '#'.join(str(x) for x in string_list)

    def convert_from_string(list_string):
        string_list = list_string.split('#')
        return_object = GyroObject(
        string_list[0], #text
        [int(x) for x in string_list[1].split('_')], #y_ar
        [int(x) for x in string_list[2].split('_')], #x_ar
        [[int(x) for x in list_x.split('-')] for list_x in string_list[3].split('_')], #ride_data
        string_list[4], #ride_num
        bool(string_list[5]), #was_ended
        )
        return return_object


#go trough file - make files in list for further use
def process_csv(csv_file):
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = []
    rides = []
    ride_number = None
    time = 0
    comment = ''
    reset  = [False, False, False, False, False, False, False]
    for row in csv_reader:
        try:
            a = int(row[0])
        except:
            first = row[0]
            if first == "DATAEND":
                rides.append(RideData(ride_number, data, True))
                data = []
                time = 0
                ride_number = None
                
            elif first[:4] == "DATA":
                if ride_number is not None:
                    rides.append(RideData(ride_number, data, False))
                    data = []
                    time = 0
                    ride_number = None
                else:
                    ride_number = first[-3:]
                
            elif (first == "NONE") or (first == "RESET"):
                reset = []
                for e in row:
                    if(e == 'RESET'):
                        a = True
                    else:
                        a = False
                    reset.append(a)
            else:
                if not comment == '':
                    comment += '_' + row[0]
                else:
                    comment = row[0]
            continue  
        data.append(DataNode(time, [int(x) for x in row],comment,reset))
        reset  = [False, False, False, False, False, False, False]
        time += 1
        comment = ''
    return rides
      


def convert_to_json(rides, start_num):
    start = start_num
    object_list = {}
    for ride in rides:
        ob_dict = {"ride_number":ride.ride_number, "was_complete":ride.wasEnded, "data":[DataNode.encode(x) for x in ride.dataArray]}
        ob_dict = str(ob_dict)
        graph_json = graph(Gyro(ride))
        object_list[start] = {'ob_dict' : ob_dict, 'graph':graph}
        start_num += 1

def add_to_json(json_dict, rides):
    keys_list = json_dict.keys()
    if len(json_dict) == 0:
        start_num = 0
    else:
        start_num = int(sorted(keys_list)[-1])+1
    added_dict = convert_to_json(rides, start_num)
    json_dict.update(added_dict)
    return json_dict

def write_to_json(json_data, ride_array):
    json_f = open(json_data, mode='r+')
    json_str = json_f.read()
    if(json_str == ''):
        json_dict = {}
    else:
        json_dict = json.loads(json_str)
    add_to_json(json_dict, ride_array)
    json_f.seek(0)
    json_f.truncate()
    json_f.write(json.dumps(json_dict))

def weird_division(n, d):
    return n / d if d else 0

def Gyro(ride):
    # sin -> x cos -> y
    text, y_ar, x_ar, other_data_ar = [], [], [], []
    rotationsA, rotationsB, x, y, gyro_background, gyro = 0, 0, 0, 0, 0, 0
    ride_num = ride.ride_number
    was_ended = ride.wasEnded
    for d in ride.dataArray: #d as data
        text.append(d.com)
        rotationsB = (abs(d.dataArray[1])- abs(rotationsB))*weird_division(abs(d.dataArray[3]), d.dataArray[3])
        rotationsA = (abs(d.dataArray[2])- abs(rotationsA))*weird_division(abs(d.dataArray[4]), d.dataArray[4])
        if sum(d.reset) is not 0:
            if d.reset[0]:
                gyro_background =+ gyro
            if d.reset[1]:
                rotationsB = abs(d.dataArray[1])*weird_division(abs(d.dataArray[3]), d.dataArray[3])
            if d.reset[2]:
                rotationsA = abs(d.dataArray[2])*weird_division(abs(d.dataArray[4]), d.dataArray[4])
        gyro = d.dataArray[0] + gyro_background
        average_rotations = (rotationsA + rotationsB)/float(2)
        x = math.sin(math.radians(gyro))*average_rotations + x
        y = math.cos(math.radians(gyro))*average_rotations + y
        other_data = d.dataArray
        y_ar.append(y)
        x_ar.append(x)
        other_data_ar.append(other_data)
    return GyroObject(text, y_ar, x_ar, other_data_ar, ride_num, was_ended)

color_dict = {
    0 : '#fb00fb', #blank, using pink for blank
    1 : '#000000', #black
    2 : '#0000FF', #blue
    3 : '#008000', #green
    4 : '#FFFF00', #yellow
    5 : '#FF0000', #red
    6 : '#FFFFFF', #white
    7 : '#A52A2A' #brown

}
def graph(GyroObject):
    source = ColumnDataSource(data = dict(
        x=GyroObject.x_ar,
        y=GyroObject.y_ar,
        color_sen_1 = [color_dict[x[5]] for x in GyroObject.other_data_ar],
        color_sen_3 = [color_dict[x[6]] for x in GyroObject.other_data_ar],
        speed_B = [x[3] for x in GyroObject.other_data_ar],
        speed_C = [x[4] for x in GyroObject.other_data_ar],
        com = GyroObject.text
    ))

    TOOLTIPS = [
        ("time", "$index"),
        ("color sensor 1", "$color[swatch]:color_sen_1"),
        ("color sensor 3", "$color[swatch]:color_sen_3"),
        ("speed on motor B", "@speed_B"),
        ("speed on motor C", "@speed_C"),
        ("comments", "@com")]

    end_dict = {
        True : "was ended",
        False : "wasn't ended"}
    p = figure(plot_width=400, plot_height=400, tooltips=TOOLTIPS, title='Ride {0} that {1}'.format(GyroObject.ride_num, end_dict[GyroObject.was_ended]), 
    x_axis_label='x (in degrees)', y_axis_label='y (in degrees)')

    p.circle('x', 'y', size=8, source=source)
    p.line(x=GyroObject.x_ar, y = GyroObject.y_ar, line_color='#00BFFF', line_width=3)

    CDN = Resources(mode="cdn")
    item_text = file_html(p, CDN, "my plot")
    return item_text
    




            
        

    
        

