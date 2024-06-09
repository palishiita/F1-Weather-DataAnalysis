import csv
import re

def getFile(path):
    rows=[]
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
        return rows;

def divideFile(data, dateRow):
    regex_pattern = r'\d\d\d\d'
    header = data[0]
    batch1 = [header]
    batch2 = [header]
    batch3 = [header]

    for row in data[1:]:
        date = re.findall(regex_pattern, row[dateRow])
        date=''.join(date)
        if date<'2000': batch1.append(row)
        elif date<'2010': batch2.append(row)
        else: batch3.append(row)
    print(batch2)
    return (batch1, batch2,batch3)



def createNewFile(filePath, data):
    with open(filePath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == '__main__':
    #NAMES OF THE FILES WITH DATES (THERE IS MORE)
    files = [
        {'name':'races', 'dateColumn':5},
        {'name':'weather', 'dateColumn':7}
    ]


    #PATHS
    path = "C:/Users/mikus/Desktop/PWR/6/Data Warehouses/project/dataset/"
    myPath = "C:/Users/mikus/Desktop/PWR/6/Data Warehouses/project/"
    pathtoDatased = "C:/Users/mikus/Desktop/PWR/6/Data Warehouses/project/dataset/"

    batchesFolders = [
        myPath + "batch1/",
        myPath + "batch2/",
        myPath + "batch3/"
    ]

    for file in files:
        batches = divideFile(getFile(path+file['name']+".csv"),file['dateColumn'])
        for i in range(0,3):
            createNewFile(batchesFolders[i]+file['name']+f"{i+1}.csv", batches[i])
