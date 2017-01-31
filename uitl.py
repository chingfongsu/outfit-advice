'''
Created on Dec 20, 2016

@author: cfsu
'''
import json
import requests
import random
from PIL import Image
from resizeimage import resizeimage
import cStringIO
import boto
from boto.s3.key import Key
import csv
import os


synonyms = ['beautiful', 'cute', 'delicate', 'elegant', 'fine',
            'gorgeous', 'lovely', 'magnificent', 'pretty', 'wonderful',
            'charming', 'delightful'
            ]

IMAGE_S3_BUCKET = 'pv-advice'
IMAGE_SIZE = [720, 480]
COLOR_FILE = 'color.csv'
COLOR_DICT = {}

def build_color_dict(dir='.'):
    global COLOR_DICT
    with open(os.path.join(dir, COLOR_FILE), mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        color_dict = { rows[0]:rows[1] for rows in reader}
    
    COLOR_DICT = color_dict
    return color_dict

def get_product_color(id):
    global COLOR_DICT
    if COLOR_DICT == {}:
        COLOR_DICT = build_color_dict()
    r = requests.get('http://api.polyvore.com/1.0/thing/'+ str(id) + '/colors')
    r_json = r.json()
    return COLOR_DICT[r_json['content'][str(id)][0]['value']]
    

class PolyvoreSet(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        self.id = int(params['id'])
        self.title = params['title']
        self.creator = params['creator']
        self.img_url= params['img_url']
        self.resized_img_url = params['resized_img_url']

class PolyvoreProduct(object):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self.id = int(params['id'])
        self.title = params['title']
        self.category_id = params['category_id']
        self.retailer = params['retailer']
        self.brand= params['brand']
        self.anchor= params['anchor']
        self.seo_term= params['seo_term']
        self.color= params['color']


def pick_set_from_trend_json(json_str, index=0):
    params = {}
    if json_str == "":
        return None
    else:
        r_json = json.loads(json_str)
        params['title'] =  r_json['content']['items'][index]['title']
        params['id'] = r_json['content']['items'][index]['items'][0]['id']
        params['creator'] = r_json['content']['items'][index]['items'][0]['creator']['name']
        params['img_url'] = r_json['content']['items'][index]['items'][0]['img_urls']['l']
        params['resized_img_url'] = 'https://s3-us-west-2.amazonaws.com/pv-advice/' + str(params['id']) + '.jpg'

        p_set = PolyvoreSet(params)
        return p_set

def pick_set_ids_from_trend_json(json_str):
    params = {}
    set_ids = []
    if json_str == "":
        return None
    else:
        r_json = json.loads(json_str)
        index = 0

        while (True):
            try:
                dummy = r_json['content']['items'][index]
            except:
                break
            set_ids.append(r_json['content']['items'][index]['items'][0]['id'])
            index += 1            
    return set_ids


def fetch_wear_trend():
    r = requests.get('http://api.polyvore.com/trend/wear/stream')
    json_str = json.dumps(r.json())
    return json_str

def upload_wear_trend_images(set_ids):
    for id in set_ids:        
        orig_img_url = 'http://ak1.polyvoreimg.com/cgi/img-set/cid/' + str(id) + '/size/y.jpg'
        new_img = image_resize(orig_img_url, IMAGE_SIZE)
        print "upload image of set id: {}".format(id)
        copy_image_to_s3(IMAGE_S3_BUCKET, new_img, str(id) + '.jpg')


def fetch_set_details(id):
    print id
    r = requests.get('http://api.polyvore.com/1.0/set/' + str(id))
    json_str = json.dumps(r.json())
    return json_str


def parse_product_in_the_set(json_str, index=0):
    params = {}
    if json_str == "":
        return None
    else:
        r_json = json.loads(json_str)
        params['id'] =  r_json['content']['things'][index]['object']['id']
        params['title'] =  r_json['content']['things'][index]['object']['title']
        params['category_id'] =  r_json['content']['things'][index]['object']['category_id']
        params['retailer'] =  r_json['content']['things'][index]['object']['host']['display_url']
        params['brand'] = r_json['content']['things'][index]['object']['brand']
        params['anchor'] = get_product_anchor(params['id'])
        params['seo_term'] = get_product_anchor(params['id'])
        params['color'] = get_product_color(params['id'])
 
        p_product = PolyvoreProduct(params)
        return p_product
    
def pick_products_from_set(json_str):
    return [parse_product_in_the_set(json_str, 0), 
            parse_product_in_the_set(json_str, 1),
            parse_product_in_the_set(json_str, 2)]


def get_product_details(id):
    r = requests.get('http://api.polyvore.com/1.0/thing/'+ str(id))
    r_json = r.json()
    return r_json

def get_product_anchor(id):
    r_json = get_product_details(id)
    return r_json['content']['breadcrumb'][-1]['anchor']

def get_product_seo_term(id):
    r = requests.get('http://api.polyvore.com/1.0/thing/'+ str(id) + '/related_searches')
    r_json = r.json()
    return r_json['content'][0]['term']

def get_category_name(id):
    r = requests.get('http://api.polyvore.com/1.0/category/' + str(id) )
    name = r.json()['content']['title']
    return name

def trim_string_by_words(s, n):
    return " ".join( s.split()[:n] )

def pick_random_adj():
    return synonyms[random.randint(0, len(synonyms)-1)] + ' '

def image_resize(url, dimensions):
    with Image.open(requests.get(url, stream=True).raw) as image:
        cover = resizeimage.resize_cover(image, dimensions)
    
    return cover

def copy_image_to_s3(bucket_name, img, file_name):
    img_out = cStringIO.StringIO()
    img.save(img_out, 'JPEG')
    #setup the bucket
    conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name, validate=False)
    img_file = Key(bucket)
    img_file.key = file_name
    img_file.content_type = "image/jpeg"
    img_file.set_contents_from_string(img_out.getvalue(), policy='public-read')
    
def del_image_on_s3(bucket_name, file_name):
    conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name, validate=False)
    img_file = Key(bucket)
    img_file.key = file_name
    bucket.delete_key(img_file)

