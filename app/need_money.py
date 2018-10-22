from pymessenger.bot import Bot
import time, requests, json

ACCESS_TOKEN = 'EAAgxZBvF1d4cBANc3Lr1wf7nfUlnyBRAU0uASBSEzkoD2tnEyYv6mPkqHLq5MjYgydy9Npa3i0WTtLovZBEY8Avf3uJP6L0MnzZCnaQMGiuMHlsjJ3imzG2tfXG9cjbvyyJhVEHXC3eJvNsq6auxMyc8LEufEeDbuPj04kZAbFvlugghdbXg'
VERIFY_TOKEN = 'treblelab'
bot = Bot(ACCESS_TOKEN)

### Constants
CONST_SAVE_MONEY = 'SaveMoney'
CONST_NEED_MONEY = 'NeedMoney'
CONST_LEARN_MONEY = 'LearnMoney'

CONST_INVEST = 'Invest'
CONST_BORROW = 'Borrow'
CONST_OTHERS = 'Others'

CONST_YES = 'Yes'
CONST_NO = 'No'

CONST_ONETIMESPEND = 'One-time big-time spend?'
CONST_INVESTMENT_ANSWERS = [CONST_ONETIMESPEND, 'Annual big expense?', 'Protection?',
                            'Retirement?', 'Just grow my money', 'Others']

CONST_TARGET_WEALTH = 'Target Wealth'
CONST_TIME_FRAME = 'Time Frame'
CONST_INITIAL_WEALTH = 'Initial Wealth'
CONST_INVEST_CONFIRM = 'Invest Confirm'
CONST_GOAL_PROBABILITY = 'Goal Probability'

###

def quick_reply_template(text, choices):
    return {
        "text": text,
        "quick_replies":choices
    }

def get_name(recipient_id):
    url = "https://graph.facebook.com/{}?fields=first_name&access_token={}".format(recipient_id, ACCESS_TOKEN)
    r = requests.get(url)
    return json.loads(r.content)['first_name']

def option_init(recipient_id):
    texts = ['''We can discuss money matters with you.''']
    for text in texts:
        bot.send_text_message(recipient_id, text)

    choices = []
    for choice in [CONST_INVEST, CONST_BORROW, CONST_OTHERS]:
        choices.append(
            {
                "type": "postback",
                "title": choice,
                "payload": CONST_NEED_MONEY+"_"+choice
            }
        )
    bot.send_button_message(recipient_id, "What do you want to discuss?", choices)

def parse_postbacks(ContextStack, recipient_id, postback):
    '''
    Parses the postback event that was triggered.
    '''
    postback_splitted = postback.split('_')

    if postback_splitted[1] == CONST_INVEST:
        texts = ['''The first step to investing is WANTING to invest. Good job!''',
                 '''Let's start with your GOALS''',
                 '''Don't worry, just chat 'Invest' later if you want to add another investment goal''',
                 '''Alright?''',
                 ]
        for text in texts:
            bot.send_text_message(recipient_id, text)
            time.sleep(0.5)

        text = 'So {}, where will you use your investment?'.format(get_name(recipient_id))
        choices = []
        for choice in CONST_INVESTMENT_ANSWERS:
            choices.append(
                {
                    "content_type": "text",
                    "title": choice,
                    "payload": CONST_NEED_MONEY+"_"+choice
                }
            )
        out = quick_reply_template(text, choices)
        bot.send_message(recipient_id, out)

    else:
        bot.send_text_message(recipient_id, 'Feature to be implemented in the future.')
    return

def parse_quickreply(ContextStack, recipient_id, response):
    
    if response[0] == CONST_ONETIMESPEND:
        texts = ['''This is Good!''',
                 '''It is always better to fund your big-time spend through investments!''',
                 '''How much is your big-time spend?''',
                 '''Please be as accurate as possible''',
                 ]
        for text in texts:
            time.sleep(0.5)
            bot.send_text_message(recipient_id, text)

        add_context(ContextStack, recipient_id, CONST_TARGET_WEALTH)
        
    elif response[0] == CONST_INVEST_CONFIRM:
        if response[1] == CONST_YES:
            name = get_name(recipient_id)
            texts = ['''Thank you for confirming!''',
                 '''You see, I am not your traditional financial advisor''',
                 '''I will not profile your risk appetites!''',
                 '''What I want to know is the probability that you think you will be able to meet this goal.''',
                 '''This will help me gauge the priority of this financial goal''',
                 '''For example, if you want to have 100% probability, I would understand that this is a priority for you.''',
                 '''You see {}, this is very important. You will be able to realize what goals are important to you'''.format(name),
                 '''On the other end, I will help you meet your goal''',
                 '''This is why I’m here anyway – to guide you. And help you achieve financial freedom!''',
                #  '''Are we clear {}'''.format(name),
                 '''So, what is it, {}? what is the probability of meeting your goal? (0-100)'''.format(name)
                 ]
            for text in texts:
                time.sleep(0.5)
                bot.send_text_message(recipient_id, text)
            add_context(ContextStack, recipient_id, CONST_GOAL_PROBABILITY)
            return 
        else:
            bot.send_text_message(recipient_id, 'Okay!')

    else:
        bot.send_text_message(recipient_id, 'Thanks!')

def add_context(ContextStack, recipient_id, context):
    if recipient_id not in ContextStack:
        ContextStack[recipient_id] = []
    print(ContextStack)
    ContextStack[recipient_id].append([CONST_NEED_MONEY,context])

def handle_user_context(ContextStack, recipient_id, response):
    last_context = ContextStack[recipient_id][-1]
    print(ContextStack)
    
    if last_context[1] == CONST_TARGET_WEALTH:
        if response.isdigit():
            num = int(response)
            if num>0:
                last_context.append(num)
                texts = ['''Okay, when will you need this money?''',
                         '''Starting from today please, in terms of days.'''
                        ]
                for text in texts:
                    time.sleep(0.5)
                    bot.send_text_message(recipient_id, text)
                add_context(ContextStack, recipient_id, CONST_TIME_FRAME)
                return
        bot.send_text_message(recipient_id, 'Try again! Make sure to type a positive number')

    elif last_context[1] == CONST_TIME_FRAME:
        if response.isdigit():
            num = int(response)
            if num>0:
                last_context.append(num)
                texts = ['''Nice! So how much is your initial investment?''',
                         '''Again, please be as accurate as possible'''
                        ]
                for text in texts:
                    time.sleep(0.5)
                    bot.send_text_message(recipient_id, text)
                add_context(ContextStack, recipient_id, CONST_INITIAL_WEALTH)
                return
        bot.send_text_message(recipient_id, 'Try again! Make sure to type a positive number')

    elif last_context[1] == CONST_INITIAL_WEALTH:
        target = ContextStack[recipient_id][0][2]
        days = ContextStack[recipient_id][1][2]
        initial = ContextStack[recipient_id][2][2]

        texts = ['''I just need to confirm.''',
                 '''You need to spend {}'''.format(target),
                 '''And you have {} days starting from today before the spend'''.format(days),
                ]
        for text in texts:
            bot.send_text_message(recipient_id, text)
            time.sleep(0.5)

        text = '''And right now, you are willing to invest {} to reach this goal'''.format(initial)
        choices = []
        for choice in [CONST_YES, CONST_NO]:
            choices.append(
                {
                    "content_type": "text",
                    "title": choice,
                    "payload": CONST_NEED_MONEY+"_"+CONST_INVEST_CONFIRM+"_"+choice
                }
            )
        out = quick_reply_template(text, choices)
        bot.send_message(recipient_id, out)

    elif last_context[1] == CONST_GOAL_PROBABILITY:
        error_msg = 'Try again! Make sure to type a value ranging from 0 to 100'
        if response.isdigit():
            num = int(response)
            if (num>=75) and (num<=100):
                bot.send_text_message(recipient_id, '''{} is a high probability. We understand that this is one of your priority goal'''.format(num))
            elif (num>=50) and (num<=74):
                bot.send_text_message(recipient_id, '''{} probability is a good start for a goal. Let’s do our best to meet this.'''.format(num))
            elif (num>=25) and (num<=49):
                bot.send_text_message(recipient_id, '''{} is a low probability. We understand you, being conservative on this aspect'''.format(num))
            elif (num>=0) and (num<=24):
                bot.send_text_message(recipient_id, '''{} is a very low probability. We understand that achieving this goal is not one of your priority'''.format(num))    
            else:
                bot.send_text_message(recipient_id, error_msg)
                return
            texts = ['''Thank you for answering all my questions.''',
                    # '''Considering this goal, we would like to recommend the following projects'''.format(target)
                    ]
            for text in texts:
                bot.send_text_message(recipient_id, text)
                time.sleep(0.5)
            
            # TODO: save responses to DB
            ContextStack.pop(recipient_id)

        bot.send_text_message(recipient_id, error_msg)

    return
