import json
import csv
import codecs
# per_name = json.load(open('./inter_res/paper_per_author.json'))
# print(len(per_name))
# for author in per_name:
#     with codecs.open('./data/all.csv', 'r', encoding='utf-8') as f:
#         f_csv = csv.reader(f)
#         for row in f_csv:
#             nums = row[2].split(',')
#             names = row[1].split(';')
#             for i in range(len(nums)):
#                 if str(nums[i]) == str(author):
#                     per_name[author] = names[i]
#                     break
#                 break




            

per_name = {}
with codecs.open('D:/WBL/networkContinue/scrap/tests/bigger_all.csv', 'r', encoding='utf-8', errors='ignore') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        nums = row[2].split(',')
        names = row[1].split(';')
        names = [n.split('(')[0] for n in names]
        if len(nums) <= len(names):
            for i in range(len(nums)):
                if nums[i] not in per_name:
                    per_name[nums[i]] = names[i]

frname = open('./inter_res/name_per_author.json', 'w', encoding='utf-8', errors='ignore')
json.dump(per_name, frname, ensure_ascii='false')