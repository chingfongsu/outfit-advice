'''
Created on Dec 20, 2016

@author: cfsu
'''
import json
import requests
import random

synonyms = ['beautiful', 'cute', 'delicate', 'elegant', 'fine',
            'gorgeous', 'lovely', 'magnificent', 'pretty', 'wonderful',
            'charming', 'delightful'
            ]

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

        p_set = PolyvoreSet(params)
        return p_set

def fetch_wear_trend():
    r = requests.get('http://api.polyvore.com/trend/wear/stream')
    json_str = json.dumps(r.json())
    return json_str

def fetch_set_details(id):
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

def get_category_name(id):
    r = requests.get('http://api.polyvore.com/1.0/category/' + str(id) )
    name = r.json()['content']['title']
    return name

def trim_string_by_words(s, n):
    return " ".join( s.split()[:n] )

def pick_random_adj():
    return synonyms[random.randint(0, len(synonyms)-1)] + ' '