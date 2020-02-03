from seletest import *
import pandas as pd

def print_data(i=None):
    for item in row_dict:
        obj = row_dict["{}, row_{}".format(listing_name, row_num)]
        obj.listing_name
        obj.r_date
        obj.r_close
        obj.r_change
        obj.r_changepercent
        obj.r_opxn
        obj.r_high
        obj.r_low
        obj.r_volume
        print("-----------------")
        #print(item, "'s value is {}".format(row_dict[item]))
