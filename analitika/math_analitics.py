
def average(GyroObject_arr):
    y = []
    x = []
    minlen = min([len(y.y_ar) for x in GyroObject_arr[0]])
    for i in range(0, minlen)):
        sum_list_x = [x.x_ar[i] for x in GyroObject_arr]
        sum_list_y = [x.y_ar[i] for x in GyroObject_arr]
        x.append(sum(sum_list_x)/len(GyroObject_arr))
        y.append(sum(sum_list_y)/len(GyroObject_arr))

    return y, x
        
        
