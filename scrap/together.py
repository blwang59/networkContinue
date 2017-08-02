import csv
import os
import re

# pattern = re.compile(r'.*csv$')
# for files in os.listdir('.'):
#     if os.path.isfile(files) and pattern.match(files):
with open('C:/Users/Administrator.WIN-C4UPVO2L26B/Desktop/results/AAAIs.csv', encoding='utf-8') as f:
    with open('./tests/bigger_all.csv', 'a+', encoding='utf-8', newline='') as wf:
        f_csv = csv.reader(f)
        fw_csv = csv.writer(wf)
        for row in f_csv:
            fw_csv.writerow(row)


