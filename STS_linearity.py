
import json
import os
import math

with_resistor_data = []
file1 = "with resistor/"

no_resistor_data = []
file2 = "no resistor/"

VIS_STS_SERIAL_NUM = "STSV0_S09004"
NIR_STS_SERIAL_NUM = "STSN0_S08887"

def get_raw_data(file, store):
    for filename in os.listdir("linearity of STS/" + file):
        with open("linearity of STS/" + file + filename) as d:
            data = []
            for item in d:
                data.append(json.loads(item))
            d.close()
            store.append(data)
            
def extract_STS_data(data_list):
    result = []
    for intensity in data_list:
        sts_data = []
        header_data = intensity[1]
        intTime = header_data['integrationTime']

        for item in intensity:
            if item.has_key("wavelengths"):
                dict = {"wavelengths": item['wavelengths'], "Halogen": item['Halogen'],
                        "serialnum": item['serialnum'], "integrationTime": intTime}
                sts_data.append(dict)

        result.append(sts_data)
        
    return result

def order_integrationTime(list):
    result = sorted(list, key=lambda k: k[1]['integrationTime'])
    return result

def order_data(list):
    NIR_STS = []
    VIS_STS = []
    for item in list:
        if item['serialnum'] == VIS_STS_SERIAL_NUM:
            VIS_STS.append(item)
        if item['serialnum'] == NIR_STS_SERIAL_NUM:
            NIR_STS.append(item)
            
    NIR_STS = sorted(NIR_STS, key=lambda k: k['wavelengths'])
    VIS_STS = sorted(VIS_STS, key=lambda k: k['wavelengths'])
    result = []
    result.append(VIS_STS)
    result.append(NIR_STS)
    return result

def find_linearity(x, wavelength, y):
    #x = integration_times
    #y = response_magnitude
    
    n = len(x)
    intercept_numerator = (sum(y)*(sum(square_list(x))))-(sum(x) * dot_product(x, y))
    denominator = (n*sum(square_list(x))) - sum(x)*sum(x)
    slope_numerator = (n*dot_product(x, y)) - (sum(x)*sum(y))
    
    slope = slope_numerator/denominator
    intercept = intercept_numerator/denominator
    
    r = (n*dot_product(x, y) - (sum(x)*sum(y))) / (math.sqrt((n*sum(square_list(x)) - (sum(x)*sum(x)))
                                                               *(n*sum(square_list(y)) - (sum(y)*sum(y)))))
    r_squared = r*r
    
    return {"wavelength": wavelength, "slope": slope, "intercept": intercept, "r_squared": r_squared}
    
def square_list(list):
    return [i**2 for i in list]

def dot_product(x, y):
    return sum(i[0] * i[1] for i in zip(x, y))
    
#def linear_regression(x, y):
    
#main program begins here    
                
x = [1, 2, 3, 4]
y = [2, 4, 6, 8]

#print(find_linearity(x, 100, y))
#raw_input(".")
        
            
get_raw_data(file1, with_resistor_data)
get_raw_data(file2, no_resistor_data)

STS_data1 = extract_STS_data(with_resistor_data)
STS_data2 = extract_STS_data(no_resistor_data)

ordered_data = []
    
STS_data1 = order_integrationTime(STS_data1)

for item in STS_data1:
    new = order_data(item)
    ordered_data.append(new)

a = []

for i in range(0, 1024):
    a.append([])
    for j in range(0, 2):
        a[i].append([])
        for k in range(0, 3):
            a[i][j].append([])

linearity_NIR = []
linearity_VIS = []

for intensity in range(0, len(ordered_data)): 
    for STS_type in range(0, len(ordered_data[intensity])):
        for dataPoint in range(0, len(ordered_data[intensity][STS_type])):
            (a[dataPoint][STS_type][0]).append(ordered_data[intensity][STS_type][dataPoint]['integrationTime'])
            (a[dataPoint][STS_type][1]).append(ordered_data[intensity][STS_type][dataPoint]['wavelengths'])
            (a[dataPoint][STS_type][2]).append(ordered_data[intensity][STS_type][dataPoint]['Halogen'])
            

for i in range(0, 1024):
    for j in range(0, 2):
        result = find_linearity(a[i][j][0], a[i][j][1][0], a[i][j][2])
        if j==0:
            linearity_NIR.append(result)
        if j==1:
            linearity_VIS.append(result)
            
with open("NIR_linearity.txt", 'w') as f:
    for item in linearity_NIR:
        json.dump(item, f)
        f.write('\n')
    f.close()

with open("VIS_linearity.txt", 'w') as f:
    for item in linearity_VIS:
        json.dump(item, f)
        f.write('\n')
    f.close()
            

            


    


    









    
        
        

