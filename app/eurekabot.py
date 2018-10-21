from flask import Flask, request, jsonify, json, url_for, redirect, session, render_template
from pymessenger.bot import Bot
from app import departures, directions, quiz, learn_to_save, risk_assessment_test, financial_products
import random

ACCESS_TOKEN = 'EAAgxZBvF1d4cBANc3Lr1wf7nfUlnyBRAU0uASBSEzkoD2tnEyYv6mPkqHLq5MjYgydy9Npa3i0WTtLovZBEY8Avf3uJP6L0MnzZCnaQMGiuMHlsjJ3imzG2tfXG9cjbvyyJhVEHXC3eJvNsq6auxMyc8LEufEeDbuPj04kZAbFvlugghdbXg'
VERIFY_TOKEN = 'treblelab'
bot = Bot(ACCESS_TOKEN)

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

    if postback == 'GREETINGS':
        #parse_response(recipient_id, 'Get Started')
        choices = [
            {
                "type":"postback",
                "title":"Help Me Learn How to Save",
                "payload":"MenuOption_1"
            },
            {
                "type":"postback",
                "title":"Take My Risk Assessment Test",
                "payload":"MenuOption_2"
            },
            {
                "type":"postback",
                "title":"Learn about Financial Products",
                "payload":"MenuOption_3"
            }
        ]
        bot.send_button_message(recipient_id, "Let's get started. What can i do for you?", choices)

    elif postback == 'MenuOption_1':
        # print('In Option 1')
        learn_to_save.option_init(recipient_id)
    elif postback == 'MenuOption_2':
        risk_assessment_test.option_init(recipient_id)
    elif postback == 'MenuOption_3':
        financial_products.option_init(recipient_id)
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
    if response.lower() in start:
        print('Main Menu will be displayed! :)')
        parse_postbacks(ContextStack, recipient_id, 'GREETINGS')

    else:
        send_message(recipient_id, 'Sorry. I did not understand what you have just said.')
    return

def parse_quickreply(ContextStack, recipient_id, payload, time_epoch):
    '''
    Parses the user's quick reply response.
    '''        
    print(payload)
    response_splitted = payload.split('_')

    if response_splitted[0] == 'LearnToSave':
        learn_to_save.parse_quickreply(ContextStack, recipient_id, response_splitted[1:])
        # learn_to_save.parse_quickreply(ContextStack, recipient_id, response_splitted[1:])
    elif response_splitted[0] == 'RiskAssessmentTest':
        risk_assessment_test.parse_quickreply(recipient_id, response_splitted[1:])
    elif response_splitted[0] == 'FinancialProducts':
        financial_products.parse_quickreply(recipient_id, response_splitted[1:])
    else:
        bot.send_text_message(recipient_id, 'Unhandled quick reply')
    return


def handle_user_context(ContextStack, recipient_id, response):
    last_context = ContextStack[recipient_id][-1]
    
    print('Processing context')
    print(last_context)
    
    # [Flow, Context]
    flow = last_context[0]
    if flow == 'LearnToSave':
        learn_to_save.handle_user_context(ContextStack, recipient_id, response)
    elif flow == 'RiskAssessmentTest':
        pass
    elif flow == 'FinancialProducts':
        pass
    return

