#imports
import analitics as an
import json

csv_file = open("default_dataset.csv", 'r')
rides = an.import_file(csv_file)
a, b, c, d, e, f = an.Gyro(rides[0])
json_file = an.graph(a, b, c, d, e, f)

with open('test_ok.html', 'w') as outfile:  
    outfile.write(json_file)



            
        

    
        

