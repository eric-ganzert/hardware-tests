
import json
import os

no_resistor_data = []
file1 = "with resistor/"

with_resistor_data = []
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

#def linear_regression(x, y):
    
    
                
        
            
get_raw_data(file1, no_resistor_data)
get_raw_data(file2, with_resistor_data)

STS_data1 = extract_STS_data(no_resistor_data)
#print(len(STS_data1))
STS_data2 = extract_STS_data(with_resistor_data)

ordered_data = []

for item in STS_data1:
    new = order_data(item)
    ordered_data.append(new)

a = []

for i in range(0, 1024):
    a.append([])
    for j in range(0, 10):
        a[i].append([])
        for k in range(0, 2):
            a[i][j].append([])
        
print(len(a))
print(len(a[0]))
    
for intensity in range(0, len(ordered_data)): 
    for STS_type in range(0, len(ordered_data[intensity])):
        for dataPoint in range(0, len(ordered_data[intensity][STS_type])):
            a[dataPoint][intensity][0].append(ordered_data[intensity][STS_type][dataPoint]['wavelengths'])
            a[dataPoint][intensity][1].append(ordered_data[intensity][STS_type][dataPoint]['Halogen'])
    
print(a[0][0][0])
raw_input(".")
            #print(ordered_data[intensity][STS_type][dataPoint])
            #raw_input(".")
            


    


    









    
        
        

