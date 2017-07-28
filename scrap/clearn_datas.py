import csv
import re
ranges = [
    {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
    {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
    {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
    {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
    {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Kana
    {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
    {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
    {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
    {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
    {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
    {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
    {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]


def is_cjk(char):
    return any([range["from"] <= ord(char) <= range["to"] for range in ranges])


def is_cjk_string(string):
    # i = 0
    # while i<len(string):
    #     if is_cjk(string[i]):
    #         return True
    #   # start = i
    #   # while is_cjk(string[i]): i += 1
    #   # yield string[start:i]
    # i += 1
    for i in string:
        if is_cjk(i):
            return True
    return False


def tell_if_cs(lists):
    l = lists.split(';')
    for i in l:
        if i == 'computer science' or i == 'data mining':
            return True
    return False

def tell_if_reports(title):
    # pattern = re.compile(r'.*((R|r)eport)|((W|w)orkshop)|(KDD)|((p|P)roceedings).*')
    pattern = re.compile(r'(.$)|')
    if pattern.match(title):
        return True
    return False


with open('C:/Users/Administrator.WIN-C4UPVO2L26B/Desktop/del_japaneses/KDD_after.csv', encoding='utf-8') as f:
    with open('./del_reports/KDD_selected.csv', 'w', encoding='utf-8', newline='') as wf:
        f_csv = csv.reader(f)
        fw_csv = csv.writer(wf)
        for row in f_csv:
            # if (is_cjk_string(row[1]) is False):
            # if tell_if_cs(row[-1]) is True:
            if tell_if_reports(row[0]) is False :
                fw_csv.writerow(row)





