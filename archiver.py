from scanner import *
import pandas as pd




def print_data():
    item_numb = 0
    row_num = 2
    for item in row_dict:
        obj = row_dict["{}, row_{}".format(identity[item_numb], row_num)]
        print('Name:', obj.name)
        print('Date:', obj.date)
        print('Close:', obj.close)
        print('Change:', obj.change)
        print('Change Percentage:', obj.changepercent)
        print('Open:', obj.opxn)
        print('High:', obj.high)
        print('Low:', obj.low)
        print('Volume:', obj.volume)
        print("-----------------")
        item_numb +=1
        row_num +=1
        #print(item, "'s value is {}".format(row_dict[item]))
