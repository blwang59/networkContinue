import json
import csv
import codecs


per_name = {}
with codecs.open('D:/WBL/networkContinue/scrap/tests/all0808_new.csv', 'r', encoding='utf-8', errors='ignore') as f:
    f_csv = csv.reader(f)
    n=1
    for row in f_csv:
        nums = row[2].split(',')
        names = row[1].split(';')
        names = [n.split('(')[0].strip() for n in names]

        # if len(nums) != len(names)-1:
        #     print(row[0]+':'+ row[5])

        # print(n)
        # # if len(nums) <= len(names):
        # print('nums:'+str(len(nums))+'names'+str(len(names))+str(nums))
        for i in range(len(nums)):
            if nums[i] not in per_name:
                per_name[nums[i]] = names[i]
        # n += 1

fr = open('./inter_res/name_per_author.json', 'w', encoding='utf-8', errors='ignore')
json.dump(per_name, fr, ensure_ascii='false')
