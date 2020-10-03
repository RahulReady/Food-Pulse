import csv

datas=[]

with open('ubereats.csv') as f:
    reader = csv.reader(f)
    data = list(reader)
    datas = [x for l in data for x in l]
    datas = [item.lower() for item in datas]
    datas = list(set(datas))

with open('ubereats_cleaned.csv', 'w') as f:
    writer = csv.writer(f)
    for data in datas:
        writer.writerow([data])
