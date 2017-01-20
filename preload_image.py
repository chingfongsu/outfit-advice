'''
Created on Jan 20, 2017

@author: cfsu
'''

from uitl import fetch_wear_trend, pick_set_ids_from_trend_json, upload_wear_trend_images

if __name__ == '__main__':
    trend_str = fetch_wear_trend()
    set_ids = pick_set_ids_from_trend_json(trend_str)
    upload_wear_trend_images(set_ids)