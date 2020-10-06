import csv

datas=[]

UBER_EATS_CSV = 'ubereats.csv'
UBER_EATS_CLEANED_CSV = 'ubereats_cleaned.csv'

with open(UBER_EATS_CSV) as f:
    reader = csv.reader(f)
    data = list(reader)
    datas = [x for l in data for x in l]
    datas = [item.lower() for item in datas]
    datas = list(set(datas))

with open(UBER_EATS_CLEANED_CSV, 'w') as f:
    writer = csv.writer(f)
    for data in datas:
        writer.writerow([data])
