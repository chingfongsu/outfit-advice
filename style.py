import logging

from random import sample, randint

from flask import Flask, render_template, jsonify

from flask_ask import Ask, statement, question, session
from __builtin__ import str

from uitl import pick_set_from_trend_json, fetch_set_details, get_category_name,\
    trim_string_by_words, pick_random_adj, build_color_dict

from uitl import PolyvoreSet, pick_set_from_trend_json, fetch_wear_trend, pick_products_from_set
from flask.templating import render_template

app = Flask(__name__)
app.config['ASK_VERIFY_REQUESTS'] = True
app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.d1b58160-99d6-4437-9b3b-839bd19d7a3f'

ask = Ask(app, "/style")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@app.errorhandler(Exception)
def unhandled_execption(e):
    app.logger.error('Unhandled Exception: %s', (e))
    response = jsonify("")
    response.status_code = 400
    return response
    

@ask.launch
def greeting():
    welcome_msg = render_template('style_welcome')
    return question(welcome_msg)        

@ask.intent("YesIntent")
def advice():
    trend_str = fetch_wear_trend()
    offset = randint(0,19)
    p_set = pick_set_from_trend_json(trend_str, offset)
    title = p_set.title
    creator = p_set.creator
    
    set_json_str = fetch_set_details(p_set.id)
    products = pick_products_from_set(set_json_str)
    advice_msg = render_template('style_outfit', 
                                 set_title=p_set.title, 
                                 set_creator=p_set.creator)
    
    advice_msg +=  render_template('style_product',
                                 prod0_cat = get_category_name(products[0].category_id),
                                 prod0_anchor = products[0].color + ' ' + trim_string_by_words(products[0].seo_term, 5),
                                 prod0_retailer = products[0].retailer,
                                 prod1_cat = get_category_name(products[1].category_id),
                                 prod1_anchor = products[1].color + ' ' + trim_string_by_words(products[1].seo_term, 5),
                                 prod1_retailer = products[1].retailer,                                 
                                 prod2_cat = get_category_name(products[2].category_id),
                                 prod2_anchor = products[2].color + ' ' + trim_string_by_words(products[2].seo_term, 5),
                                 prod2_retailer = products[2].retailer                                 

                                 )
    return statement(advice_msg) \
        .standard_card(title='Outfit of the Day',
                       text=p_set.title + ' by ' + p_set.creator,
                       small_image_url=p_set.resized_img_url,
                       large_image_url=None)

@ask.intent("NoIntent")
def no_advice():
    advice_msg = render_template('style_no_advice')
    return statement(advice_msg)


@ask.intent("AMAZON.HelpIntent")
def help_prompt():
    return question("Please say Yes, or No!")        
        
@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")

@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=False)