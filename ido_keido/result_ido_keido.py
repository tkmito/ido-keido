import requests, bs4 
import pandas as pd
import re

df = pd.read_csv('getdata.csv')
df['latitude'] = 0
df['longitude'] = 0

c_dict = {'AL':'Alabama', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 'CO':'Colorado', 'CT':'Connecticut', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan','MN':'Minnesota', 'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New_Hampshire', 'NJ':'New_Jersey', 'NM':'New_Mexico', 'NY':'New_York', 'NC':'North_Carolina', 'ND':'North_Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode_Island', 'SC':'South_Carolina', 'SD':'South_Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West_Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}

for index, row in df.iterrows():
#     print(index)
#     print(row)
    name = row.iat[2]
    name_list = name.split()
    if name == 'District of Columbia':
        url = 'https://en.wikipedia.org/wiki/Washington,_D.C.'
    elif len(name_list) == 3:
        if name_list[2] == 'LA':
            url = 'https://en.wikipedia.org/wiki/' + name_list[0] + '_Parish,_' + c_dict[name_list[2]]
        else:
            url = 'https://en.wikipedia.org/wiki/' + name_list[0] + '_' + name_list[1] + ',_' + c_dict[name_list[2]]
            
    elif len(name_list) == 4:
        if name_list[3] == 'LA':
            url = 'https://en.wikipedia.org/wiki/' + name_list[0] + '_' + name_list[1] + '_Parish,_' + c_dict[name_list[3]]
        else:
            url = 'https://en.wikipedia.org/wiki/' + name_list[0] + '_' + name_list[1] + '_' + name_list[2] + ',_' + c_dict[name_list[3]]
    
    elif len(name_list) == 5:
        if name_list[4] == 'LA':
             url = 'https://en.wikipedia.org/wiki/' + name_list[0] + '_' + name_list[1] + '_' + name_list[2] + '_Parish,_' + c_dict[name_list[4]]
        else:
            url = 'https://en.wikipedia.org/wiki/' + name_list[0] + '_' + name_list[1] + '_' + name_list[2] + '_' + name_list[3] + ',_' + c_dict[name_list[4]]
    
    elif len(name_list) == 6:
        if name_list[5] == 'LA':
            url = 'https://en.wikipedia.org/wiki/' + name_list[0] + '_' + name_list[1] + '_' + name_list[2] + '_' + name_list[3] + '_Parish,_' + c_dict[name_list[5]]
        else:
            url = 'https://en.wikipedia.org/wiki/' + name_list[0] + '_' + name_list[1] + '_' + name_list[2] + '_' + name_list[3] + '_' + name_list[4] + ',_' + c_dict[name_list[5]]
    else:
        url = 'nothing'
#     print(url)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    
    latitude=soup.select('.latitude')
    longitude=soup.select('.longitude')
    
    for i in latitude:
        str = i.getText()
        data = re.findall('[0-9]+', str)
        
        if len(data) == 3 :
            data1 = int(data[0])
            data2 = int(data[1])
            data3 = int(data[2])
        elif len(data) == 2:
            data1 = int(data[0])
            data2 = int(data[1])
            data3 = 0
        elif len(data) == 1:
            data1 = int(data[0])
            data2 = 0
            data3 = 0
            
        latidata = float(data1 + data2/60 + data3/(60*60))
        
        print("latitude   :", end = '')
        print(latidata)
        print("mimute     :", end = '')
        print(data2)
        print("second     :", end = '')
        print(data3)
        df.at[index, 'mimute'] = data2
        df.at[index, 'second'] = data3
        
    for i in longitude:
        str = i.getText()
        data = re.findall('[0-9]+', str)
        
        if len(data) == 3 :
            data1 = int(data[0])
            data2 = int(data[1])
            data3 = int(data[2])
        elif len(data) == 2:
            data1 = int(data[0])
            data2 = int(data[1])
            data3 = 0
        elif len(data) == 1:
            data1 = int(data[0])
            data2 = 0
            data3 = 0
            
        data4 = float(data1 + data2/60 + data3/(60*60))
        longdata = (data4)*-1
        
        print("longtitude :", end = '')
        print(longdata)
        print("mimute     :", end = '')
        print(data2)
        print("second     :", end = '')
        print(data3)
        df.at[index, 'latitude'] = latidata
        df.at[index, 'longitude'] = longdata
        df.at[index, 'mimute2'] = data2
        df.at[index, 'second2'] = data3
        
print(df)
#df.to_csv('result2.csv')
df.to_csv('result2.csv', float_format='%.8f')