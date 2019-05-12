from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import pickle
import math
output_file("label.html", title="label.py example")

def weird_division(n, d):
    return n / d if d else 0

def Gyro(ride):
    # sin -> x cos -> y
    text, y_ar, x_ar = [], [], []
    rotationsA, rotationsB, x, y, gyro_background, gyro = 0, 0, 0, 0, 0, 0
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
        y_ar.append(y)
        x_ar.append(x)
    return text, y_ar, x_ar


data = pickle.load( open( "listfile.data", "rb" ) ) #text, y, x

source = ColumnDataSource(data=dict(height=data[1],
                                    weight=data[2],
                                    names=data[0]))

p = figure(title='ride of robot',
           x_range=Range1d(0, 275),
           y_range=Range1d(0, 275))
           
p.scatter(x='weight', y='height', size=8, source=source)
p.xaxis[0].axis_label = 'Weight (lbs)'
p.yaxis[0].axis_label = 'Height (in)'

labels = LabelSet(x='weight', y='height', text='names', level='glyph',
              x_offset=5, y_offset=5, source=source, render_mode='canvas')



p.add_layout(labels)
show(p)