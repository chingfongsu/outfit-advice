'''
Created on Dec 20, 2016

@author: cfsu
'''
import unittest
from uitl import PolyvoreSet, pick_set_from_trend_json, fetch_wear_trend,\
    pick_products_from_set, get_category_name, trim_string_by_words,\
    get_product_anchor, pick_random_adj, image_resize, IMAGE_S3_BUCKET,\
    copy_image_to_s3, del_image_on_s3, pick_set_ids_from_trend_json, \
    upload_wear_trend_images
import requests
import json
from PIL import Image
from resizeimage import resizeimage
import boto
from boto.s3.key import Key

class test_util(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_set(self):
        s1 = PolyvoreSet({'id': 111, 'title': "A beautiful winter", 'creator': "Amy", \
                          'img_url':"none", 'resized_img_url':"none"})
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
        self.assertEqual('self-portrait dresses', anchor, 'get the wrong anchor')
        
    def test_image_resize(self):
        url = 'http://ak1.polyvoreimg.com/cgi/img-set/cid/213173733/id/pKB8lpjC5hGVEMtLtfvecw/size/y.jpg'
        dimensions = [720, 480]
        cover = image_resize(url, dimensions)
        cover.save('test-image-resized-720-480.jpg')
        new_img = Image.open('test-image-resized-720-480.jpg')
        self.assertEqual(new_img.size, (720,480), "new image is not correct size")
        
    def test_copy_image_to_s3(self):
        image = Image.open('test-image.jpg')
        copy_image_to_s3(IMAGE_S3_BUCKET, image, 'test-image.jpg')
        url = 'https://s3-us-west-2.amazonaws.com/pv-advice/test-image.jpg'
        ret = requests.head(url)
        self.assertEqual(ret.status_code, 200, "image was not uploaded successfully")
        del_image_on_s3(IMAGE_S3_BUCKET, 'test-image.jpg')

    def test_pick_set_ids_from_trend_json(self):
        with open('test_data1.json') as data_file:    
            r_json = json.load(data_file)

        json_str = json.dumps(r_json)
        set_ids = pick_set_ids_from_trend_json(json_str)
        self.assertEqual(set_ids, [120776482, 210636696, 210418711, 212123225, 212748214, 207648226, 146274963, 207705780, 208100899, 207325736, 186446024, 183145088, 175222787, 184479106, 108329971, 210854794, 211415448, 193346094, 177627693, 211099175, 212708578, 194194202, 194951944, 213107279, 204839502, 210815579, 193756075, 177885320, 137584126, 179488325] , "set IDs are not correcdt")
    
    @unittest.skip("preload images. not a test")
    def test_upload_wear_trend_images(self):
        trend_str = fetch_wear_trend()
        set_ids = pick_set_ids_from_trend_json(trend_str)
        upload_wear_trend_images(set_ids)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()