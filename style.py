import logging

from random import sample, randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session, audio
from __builtin__ import str

from twilio.rest import TwilioRestClient
from uitl import pick_set_from_trend_json, fetch_set_details, get_category_name,\
    trim_string_by_words, pick_random_adj

from uitl import PolyvoreSet, pick_set_from_trend_json, fetch_wear_trend, pick_products_from_set
from flask.templating import render_template

app = Flask(__name__)

ask = Ask(app, "/style")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def send_MMS(img_url, set_title):
    account_sid = "AC8d9789a94adb78a2ad0fcef067433ce6" # Your Account SID from www.twilio.com/console
    auth_token  = "bcb3b5a6a27f25e5d75f1ec9937a8177"  # Your Auth Token from www.twilio.com/console

    client = TwilioRestClient(account_sid, auth_token)

    note = "Polyvore Outfit" + " - " + set_title
    image = img_url
    message = client.messages.create(
        body=note,
        media_url = image,
        to="+14082214602",    # Replace with your phone number
        from_="+14083594033" # Replace with your Twilio number
    )
    print(message.sid)


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
    print products[0].id, products[1].id
    advice_msg = render_template('style_outfit', 
                                 set_title=p_set.title, 
                                 set_creator=p_set.creator)
    
    advice_msg +=  render_template('style_product',
                                 prod0_cat = get_category_name(products[0].category_id),
                                 prod0_anchor = pick_random_adj() + trim_string_by_words(products[0].anchor, 5),
                                 prod0_retailer = products[0].retailer,
                                 prod1_cat = get_category_name(products[1].category_id),
                                 prod1_anchor = pick_random_adj() + trim_string_by_words(products[1].anchor, 5),
                                 prod1_retailer = products[2].retailer,                                 
                                 prod2_cat = get_category_name(products[2].category_id),
                                 prod2_anchor = pick_random_adj() + trim_string_by_words(products[2].anchor, 5),
                                 prod2_retailer = products[1].retailer                                 

                                 )
    advice_msg +=  render_template('style_mms')
    send_MMS(p_set.img_url, p_set.title)
    return statement(advice_msg)


@ask.intent("NoIntent")
def no_advice():
    advice_msg = render_template('style_no_advice')
    return statement(advice_msg)
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

    app.run(debug=True)