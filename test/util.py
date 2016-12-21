'''
Created on Dec 20, 2016

@author: cfsu
'''
import unittest
from uitl import PolyvoreSet, pick_set_from_trend_json, fetch_wear_trend,\
    pick_products_from_set, get_category_name, trim_string_by_words,\
    get_product_anchor, pick_random_adj
import requests
import json

class test_util(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_set(self):
        s1 = PolyvoreSet({'id': 111, 'title': "A beautiful winter", 'creator': "Amy", 'img_url':"none"})
        self.assertEqual(s1.title, "A beautiful winter", "wrong title from set")
        self.assertEqual(s1.id, 111, "wrong id from set")

    def test_pick_set_from_trend_json(self):
        p_set = pick_set_from_trend_json("")
        self.assertEqual(p_set, None, "should be empty set from empty json")

        #r = requests.get('http://api.polyvore.com/trend/wear/stream')
        #r_json = r.json()
        #with open('test_data1.json', 'w') as outfile:
            #json.dump(r_json, outfile, indent=4, sort_keys=True, separators=(',', ':'))
            
        with open('test_data1.json') as data_file:    
            r_json = json.load(data_file)

        json_str = json.dumps(r_json)
        
        p_set = pick_set_from_trend_json(json_str)
        self.assertEqual('Creepers', p_set.title, 'wrong set title')
        self.assertEqual(120776482, p_set.id, 'wrong set id')


    def test_fetch_trend_wear(self):
        json_str = fetch_wear_trend()
        p_set = pick_set_from_trend_json(json_str)
        #self.assertEqual('Creepers', p_set.title, 'wrong set title')

    def test_pick_products_from_set(self):
        #r = requests.get('http://api.polyvore.com/1.0/set/120776482')
        #r_json = r.json()
        #with open('test_set_data.json', 'w') as outfile:
            #json.dump(r_json, outfile, indent=4, sort_keys=True, separators=(',', ':'))
        with open('test_set_data.json') as data_file:    
            r_json = json.load(data_file)

        json_str = json.dumps(r_json)
        
        # two products for now
        products = pick_products_from_set(json_str)
        self.assertEqual('Jeans With Cut Out Holes', products[0].title, 'wrong set title')
        self.assertEqual(106689043, products[0].id, 'wrong product id')

        self.assertEqual('T.U.K. Black Suede Mondo Creepers | Hot Topic', products[1].title, 'wrong set title')
        self.assertEqual(108695081, products[1].id, 'wrong product id')

    def test_get_category_name(self):
        name = get_category_name(27)
        self.assertEqual('Jeans', name, 'wrong category name')
        
    def test_trim_string_by_words(self):
        s = 'this is a long sentence'
        result = trim_string_by_words(s, 3)
        self.assertEqual('this is a', result, 'not trimmed properly')

    def test_get_product_anchor(self):
        with open('test_set_data.json') as data_file:    
            r_json = json.load(data_file)

        anchor = get_product_anchor(182825885)
        print anchor
        self.assertEqual('self-portrait dresses', anchor, 'get the wrong anchor')
    
    def test_pick_random_adj(self):
        print pick_random_adj()

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()