import csv
import os
import re

# pattern = re.compile(r'.*csv$')
# for files in os.listdir('C:/Users/Administrator.WIN-C4UPVO2L26B/Desktop/results/'):
#     # if os.path.isfile(files) and pattern.match(files):
#     with open('C:/Users/Administrator.WIN-C4UPVO2L26B/Desktop/results/'+files, encoding='utf-8') as f:
#         with open('D:/WBL/networkContinue/scrap/tests/all0808.csv', 'a+', encoding='utf-8', newline='') as fw:
#             f_csv = csv.reader(f)
#             fw_csv = csv.writer(fw)
#             for row in f_csv:
#                 fw_csv.writerow(row)
# pattern = re.compile(r'.*csv$')
# for files in os.listdir('C:/Users/Administrator.WIN-C4UPVO2L26B/Desktop/results/'):
#     if pattern.match(files):
with open('C:/Users/Administrator.WIN-C4UPVO2L26B/Desktop/results/WWW.csv', encoding='utf-8') as f:
# with open('D:/WBL/networkContinue/scrap/tests/all0808.csv', encoding='utf-8') as f:
    with open('D:/WBL/networkContinue/scrap/tests/all0808_new.csv', 'a+', encoding='utf-8', newline='') as fw:
        f_csv = csv.reader(f)
        fw_csv = csv.writer(fw)

        for row in f_csv:
            # if row[5] != "International World Wide Web Conferences":
            fw_csv.writerow(row)
