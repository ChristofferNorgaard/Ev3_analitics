import analitics as an
import webbrowser



file = open("data_csv/default_dataset.csv")   
a = an.process_csv(file)
old_gyro = an.Gyro(a[0])
new_gyro = an.Gyro(a[1])
x, y = an.average([old_gyro, new_gyro])
print(an.deviation([x, y], [x, y]))
html = an.graph([old_gyro, new_gyro], [x, y])
try:
    webbrowser.open(html)
except:
    pass






