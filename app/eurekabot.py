from flask import Flask, request, jsonify, json, url_for, redirect, session, render_template
from pymessenger.bot import Bot
from app import departures, directions, quiz, learn_to_save, risk_assessment_test, financial_products, need_money
import random, requests
import sqlite3 as sql

ACCESS_TOKEN = 'EAAgxZBvF1d4cBANc3Lr1wf7nfUlnyBRAU0uASBSEzkoD2tnEyYv6mPkqHLq5MjYgydy9Npa3i0WTtLovZBEY8Avf3uJP6L0MnzZCnaQMGiuMHlsjJ3imzG2tfXG9cjbvyyJhVEHXC3eJvNsq6auxMyc8LEufEeDbuPj04kZAbFvlugghdbXg'
VERIFY_TOKEN = 'treblelab'
bot = Bot(ACCESS_TOKEN)

### Constants
CONST_FIRST_TIME_USER = 'FirstTimeUser'

CONST_MENU = "MENU"
CONST_MENU_OPTION_1 = "MenuOption_1"
CONST_MENU_OPTION_2 = "MenuOption_2"
CONST_MENU_OPTION_3 = "MenuOption_3"

CONST_SAVE_MONEY = 'SaveMoney'
CONST_NEED_MONEY = 'NeedMoney'
CONST_LEARN_MONEY = 'LearnMoney'

CONST_AGE = 'Age'
CONST_OCCUPATION = 'Occupation'
CONST_INCOME = 'MonthlyIncome'
CONST_INVEST = 'Invest'

CONST_YES = 'Yes'
CONST_NO = 'No'

###

def verify_fb_token(token_sent):
    '''
    take token sent by facebook and verify it matches the verify token you sent
    if they match, allow the request, else return an error 
    '''
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_default_message():
    '''
    Default message
    '''
    msg = [
        '''Hi how are you? My name's Finko. I'm at your service
        24 hours a day, 7 days a week! Ask me anything about finance
        and investing! Huwag po kayo mahiya! I'm happy to help!
        '''
        ]
    return random.choice(msg)

def get_name(recipient_id):
    # return 'Test'
    url = "https://graph.facebook.com/{}?fields=first_name&access_token={}".format(recipient_id, ACCESS_TOKEN)
    r = requests.get(url)    
    return json.loads(r.content)['first_name']

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    '''
    sends user the text message provided via input response parameter
    '''
    bot.send_text_message(recipient_id, response)
    return

def parse_postbacks(ContextStack, recipient_id, postback):
    '''
    Parses the postback event that was triggered.
    '''
    
    postback_splitted = postback.split('_')

    if postback == CONST_FIRST_TIME_USER:
        name = get_name(recipient_id)
        texts = ['''Hi {}! I’m Finko. Need Financial Advice? I can help'''.format(name),
                 '''For me to help you better, I’m going to need to know a little more about you…''',
                 '''Don’t be shy! Whatever we discuss stays between us ;)''',
                 '''So {}, Let’s start with age. How old (or young) are you?'''.format(name)]
        for text in texts:
            bot.send_text_message(recipient_id, text)
        
        # add Age context
        add_context(ContextStack, recipient_id, CONST_AGE)

    elif postback == CONST_MENU:
        #parse_response(recipient_id, 'Get Started')
        choices = [
            {
                "type": "postback",
                "title": "Save Money",
                "payload": CONST_MENU_OPTION_1
            },
            {
                "type": "postback",
                "title": "Need Money",
                "payload": CONST_MENU_OPTION_2
            },
            {
                "type": "postback",
                "title": "Learn more about money",
                "payload": CONST_MENU_OPTION_3
            }
        ]
        bot.send_button_message(recipient_id, "Cheers. What can I help you with?", choices)

    elif postback == CONST_MENU_OPTION_1:
        # print('In Option 1')
        learn_to_save.option_init(recipient_id)
    elif postback == CONST_MENU_OPTION_2:
        # risk_assessment_test.option_init(recipient_id)
        need_money.option_init(recipient_id)
    elif postback == CONST_MENU_OPTION_3:
        financial_products.option_init(recipient_id)
        
    elif postback_splitted[0] == CONST_NEED_MONEY:
        need_money.parse_postbacks(ContextStack, recipient_id, postback)
    elif postback_splitted[0] == CONST_LEARN_MONEY:
        financial_products.parse_postbacks(ContextStack, recipient_id, postback)
    else:
        bot.send_text_message(recipient_id, 'Unhandled postback')
    return
    
def parse_response(ContextStack, recipient_id, response):
    '''
    Parses the user's response.
    '''     
    # Check if the response is an answer to a previous question
    if recipient_id in ContextStack:
        handle_user_context(ContextStack, recipient_id, response)
        return

    start = ['start', 'ok', 'good morning', 'good afternoon', 
    'good evening', 'game', 'g', 'yes', 'hi', 'hello', 'hey']
    #intro = ['intro']
    # if response.lower() in intro:  
    if not user_exists(recipient_id):
        parse_postbacks(ContextStack, recipient_id, CONST_FIRST_TIME_USER)
        return

    if response.lower() == 'invest':
        parse_postbacks(ContextStack, recipient_id, CONST_NEED_MONEY+'_'+CONST_INVEST)
    
    elif response.lower() in start:
        # print('Main Menu will be displayed! :)')
        parse_postbacks(ContextStack, recipient_id, CONST_MENU)

    else:
        send_message(recipient_id, 'Sorry. I did not understand what you have just said.')
    return

def parse_quickreply(ContextStack, recipient_id, payload, time_epoch):
    '''
    Parses the user's quick reply response.
    '''        
    print(payload)
    response_splitted = payload.split('_')

    # handle rare cases that can cause error
    if len(response_splitted) < 2:
        print('No Context')
        return

    if response_splitted[0] == CONST_SAVE_MONEY:
        learn_to_save.parse_quickreply(ContextStack, recipient_id, response_splitted[1:])
    elif response_splitted[0] == CONST_NEED_MONEY:
        # risk_assessment_test.parse_quickreply(recipient_id, response_splitted[1:])
        need_money.parse_quickreply(ContextStack, recipient_id, response_splitted[1:])
    elif response_splitted[0] == CONST_LEARN_MONEY:
        financial_products.parse_quickreply(recipient_id, response_splitted[1:])
    elif response_splitted[0] == CONST_FIRST_TIME_USER:
        if response_splitted[1] == CONST_INCOME:
            print('ContextStack:',ContextStack)
            if recipient_id in ContextStack:
                if len(ContextStack[recipient_id]) == 2:
                    # TODO: save responses to DB
                    ## Add to DB
                    income = response_splitted[2]
                    occupation = ContextStack[recipient_id].pop()[2]
                    age = ContextStack[recipient_id].pop()[2]
                    add_user(recipient_id, age, occupation, income)
                    print('Details added to database!!!')
                    ## End of DB

                ContextStack.pop(recipient_id) # empty context
            parse_postbacks(ContextStack, recipient_id, CONST_MENU)
    else:
        bot.send_text_message(recipient_id, 'Unhandled quick reply')
    return


def handle_user_context(ContextStack, recipient_id, response):
    last_context = ContextStack[recipient_id][-1]
    
    print('Processing context')
    print(last_context)
    
    # handle rare cases that can cause error
    if len(last_context) < 2:
        print('No Context')
        return

    # [Flow, Context]
    flow = last_context[0]
    if flow == CONST_SAVE_MONEY:
        learn_to_save.handle_user_context(ContextStack, recipient_id, response)
    elif flow == CONST_NEED_MONEY:
        need_money.handle_user_context(ContextStack, recipient_id, response)
        # need_money.handle_user_context(ContextStack, recipient_id, response)
    elif flow == CONST_LEARN_MONEY:
        pass
    elif flow == CONST_FIRST_TIME_USER:
        if last_context[1] == CONST_AGE:
            if response.isdigit():
                num = int(response)
                if num >= 18:
                    last_context.append(num)
                    add_context(ContextStack, recipient_id, CONST_OCCUPATION)
                    bot.send_text_message(recipient_id, 'What is your occupation?')
                    return
            bot.send_text_message(recipient_id, 'Try again! Make sure to type a number greater than 18')
        elif last_context[1] == CONST_OCCUPATION:
            last_context.append(response)
            # add_context(ContextStack, recipient_id, CONST_INCOME)

            choices = []
            for choice in ['Under 50k Pesos', '50-99k Pesos', '100-149k Pesos', '150-200k Pesos', 'Above 200k Pesos']:
                choices.append(
                    {
                        "content_type":"text",
                        "title":choice,
                        "payload":CONST_FIRST_TIME_USER+"_"+CONST_INCOME+"_"+choice
                    }
                )
            out = quick_reply_template('To help you better, please disclose your monthly income:', choices)
            bot.send_message(recipient_id, out)
            #print('Final context stack before saving to db:', ContextStack)

    return

def add_context(ContextStack, recipient_id, context):
    if recipient_id not in ContextStack:
        ContextStack[recipient_id] = []
    print(ContextStack)
    ContextStack[recipient_id].append([CONST_FIRST_TIME_USER,context])

def quick_reply_template(text, choices):
    return {
        "text": text,
        "quick_replies":choices
    }

def add_user(id, age, occupation, income):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('''INSERT INTO users (id,age,occupation,income) 
               VALUES (?,?,?,?)''',(id,age,occupation,income) )
            
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
      
    finally:
        return msg
        con.close()

def user_exists(id):
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('''SELECT * FROM users WHERE id={}'''.format(id))
        
    rows = cur.fetchall()
    return rows==True
