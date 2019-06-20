#imports
import csv
import json
import math
from bokeh.plotting import figure, output_file, show, ColumnDataSource
import bokeh as bk
import time
from bokeh.embed import file_html
from bokeh.resources import Resources
from bokeh.models import HoverTool, WheelZoomTool, BoxZoomTool, PanTool
from ast import literal_eval
#class definitions
class DataNode:
    def __init__(self, time, dataArray=[], com=None, reset=[],):
        self.time = time
        self.dataArray = dataArray # [GIRO,ROTATIONS_B,ROTATIONS_C,SPEED_B,SPEED_C,COLOR_3,COLOR_1]
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
        literal_eval(string_list[0]), #text
        [float(x) for x in string_list[1].split('_')], #y_ar
        [float(x) for x in string_list[2].split('_')], #x_ar
        [[int(y) for y in x] for x in [x.strip('][').split(', ') for x in [x + ']' for x in "".join([x.replace("_", "") for x in string_list[3].split('-')]).split("]")]][:-1]], #ride_data
        string_list[4], #ride_num
        bool(string_list[5]), #was_ended
        )
        return return_object


#go trough file - make files in list for further use
def process_csv(csv_file):
    csv_reader = csv.reader(csv_file, delimiter=';')
    data = []
    rides = []
    ride_number = None
    time = 0
    comment = ''
    reset  = [False, False, False, False, False, False, False]
    skip_mode = False
    for row in csv_reader:
        
        if skip_mode:
            if "DATA" not in row[0]:
                continue
            else:
                skip_mode = False
        try:
            a = int(row[0])
        except:
            first = row[0]
            if first == "DATAEND":
                rides.append(RideData(ride_number, data, True))
                data = []
                time = 0
                ride_number = None
                skip_mode = True
                
            elif first[:4] == "DATA":
                if ride_number is not None:
                    rides.append(RideData(ride_number, data, False))
                    data = []
                    time = 0
                    ride_number = first[-3:]
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
        print(row)
        reset  = [False, False, False, False, False, False, False]
        time += 1
        comment = ''
        
    return rides
      
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
colors = ['#32CD32', '#228B22', '#008000', '#FFA500'] #last is for avrage

def graph(GyroObjects, average_gyro_object = None):
    if len(GyroObjects) > 3:
        raise ValueError('too big array')
    ho = HoverTool(names=["foo", "bar"])
    
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
    p = figure(plot_width=400, plot_height=400, tooltips=TOOLTIPS, 
    x_axis_label='x (in degrees)', y_axis_label='y (in degrees)', tools = [ho, WheelZoomTool(), BoxZoomTool(), PanTool()])

    for i, gr in enumerate(GyroObjects):
        for x in gr.other_data_ar:
            if len(x) == 6:
                print(x)
        source = ColumnDataSource(data = dict(
        x=gr.x_ar,
        y=gr.y_ar,
        color_sen_1 = [color_dict[x[5]] for x in gr.other_data_ar],
        color_sen_3 = [color_dict[x[6]] for x in gr.other_data_ar],
        speed_B =  [x[3] for x in gr.other_data_ar],
        speed_C = [x[4] for x in gr.other_data_ar],
        com = gr.other_data_ar
        ))
        p.circle('x', 'y', size=3.5, source=source, name='foo', color=colors[i])
        p.line(x=gr.x_ar, y = gr.y_ar, line_color=colors[i], line_width=3, color=colors[i], legend='Ride {0} that {1}'.format(gr.ride_num, end_dict[gr.was_ended]))
    if average_gyro_object is not None:
        source = ColumnDataSource(data = dict(
            x = average_gyro_object[0],
            y = average_gyro_object[1]
        ))
        p.circle('x', 'y', size=3.5, source=source, name='goo', color=colors[3])
        p.line(x=average_gyro_object[0], y = average_gyro_object[1], line_color=colors[3], line_width=3)
    CDN = Resources(mode="cdn")
    item_text = file_html(p, CDN, "my plot")
    #show(p)
    return item_text
# math tools
def average(GyroObject_arr):
    y = []
    x = []
    average_len = sum([len(x.x_ar) for x in GyroObject_arr])/len(GyroObject_arr)
    for i in range(0, int(average_len)):
        sum_list_x = [x.x_ar[i] for x in GyroObject_arr if i < len(x.x_ar)]
        sum_list_y = [x.y_ar[i] for x in GyroObject_arr if i < len(x.x_ar)]
        x.append(sum(sum_list_x)/len(sum_list_x))
        y.append(sum(sum_list_y)/len(sum_list_y))
    return x, y    

def deviation(sample, reference):
    ''' 
    sample = [x ,y]
    reference = [x, y]
    '''
    addedsquares = 0
    for i in range(0, len(reference)):
        try:
            x = (sample[0][i] - reference[0][i])**2
            y = (sample[1][i] - reference[1][i])**2
        except:
            x = (reference[0][i])**2
            y = (reference[1][i])**2
        addedsquares += x + y
    return math.sqrt(addedsquares/len(reference))
test = True


            
        

    
        

