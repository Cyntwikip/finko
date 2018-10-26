from pymessenger.bot import Bot

ACCESS_TOKEN = 'EAAaJ7bi0JewBAIbQqgm3GnIrcGB8MJdFY6LGmwjZC4k2QIdQXUMkr6PAlsEBqElNFb9SGauDHukQ890j7rxZBRJDnlyJdZBgOKCcrLkRRK9Tu6zcKq1oqMVMZCsjXvc69FTTuVmgejZC3uhFfL3jnfZCZBkhyCWS2DFj5RL6tAHA4HZBBeQf2sVu'
VERIFY_TOKEN = 'treblelab'
bot = Bot(ACCESS_TOKEN)

### Constants
CONST_SAVE_MONEY = 'SaveMoney'
CONST_NEED_MONEY = 'NeedMoney'
CONST_LEARN_MONEY = 'LearnMoney'

CONST_MENU_OPTION_2 = "MenuOption_2"
CONST_MENU_OPTION_3 = "MenuOption_3"

CONST_MONDAY_AM_TIME = 'Monday AM Time'
CONST_FRIDAY_PM_TIME = 'Friday PM Time'
CONST_EVERY_MONDAY_AM = 'Every Monday AM'
CONST_EVERY_FRIDAY_PM = 'Every Friday PM'
CONST_TIME_CONFIRM = 'TimeConfirm'
CONST_YES = 'Yes'
CONST_NO = 'No'

###

def quick_reply_template(text, choices):
    return {
        "text": text,
        "quick_replies":choices
    }

def option_init(recipient_id):
    texts = ['''Am glad to hear that you want to learn how to save!''',
            '''Yes, it is very important to set aside money for emergencies and also for future investments''',
            '''Sometimes, it is a matter of remembering that you need to save today!''']
    for text in texts:
        bot.send_text_message(recipient_id, text)

    choices = []
    for choice in [CONST_YES, CONST_NO]:
        choices.append(
            {
                "content_type": "text",
                "title": choice,
                "payload": CONST_SAVE_MONEY+"_"+choice
            }
        )
        
    out = quick_reply_template('Do you want me to remind you to save on a weekly basis?', choices)
    bot.send_message(recipient_id, out)


def parse_quickreply(ContextStack, recipient_id, response):
    if response[0] == CONST_NO:
        bot.send_text_message(recipient_id, 'Got it!')

    elif response[0] == CONST_YES:
        text = 'Got it! When do you want me to remind you? Salamat'
        choices = []
        for choice in [CONST_EVERY_MONDAY_AM, CONST_EVERY_FRIDAY_PM]:
            choices.append(
                {
                    "content_type": "text",
                    "title": choice,
                    "payload": CONST_SAVE_MONEY+"_Day_"+choice
                }
            )
        out = quick_reply_template(text, choices)
        bot.send_message(recipient_id, out)

    # elif response[0] == 'Day':
    #     bot.send_text_message(recipient_id, 'You have selected '+response[1])

    elif response[0] == 'Day' and response[1] == CONST_EVERY_MONDAY_AM:
        add_context(ContextStack, recipient_id, CONST_MONDAY_AM_TIME)
        bot.send_text_message(recipient_id, 'What time in the morning?')

    elif response[0] == 'Day' and response[1] == CONST_EVERY_FRIDAY_PM:
        add_context(ContextStack, recipient_id, CONST_FRIDAY_PM_TIME)
        bot.send_text_message(recipient_id, 'What time in the afternoon/evening?')

    elif response[0] == CONST_TIME_CONFIRM:
        if response[1] == CONST_YES:
            last_context = ContextStack[recipient_id][-1]
            if last_context[1] == CONST_MONDAY_AM_TIME:
                text = 'every Monday, {} AM'.format(last_context[-1])
            elif last_context[1] == CONST_FRIDAY_PM_TIME:
                text = 'every Friday, {} PM'.format(last_context[-1])
            ContextStack.pop(recipient_id) # empty context
            bot.send_text_message(recipient_id, 'Got it! I will remind you {}'.format(text))

            text = 'Do you want to invest now?... Or do you want to learn more about investing? Salamat!'
            choices = []
            for title, payload in zip(['Invest Now', 'Learn More'], [CONST_MENU_OPTION_2, CONST_MENU_OPTION_3]):
                choices.append(
                    {
                        "content_type": "text",
                        "title": title,
                        "payload": payload
                    }
                )
            out = quick_reply_template(text, choices)
            bot.send_message(recipient_id, out)

        elif response[1] == CONST_NO:
            ContextStack.pop(recipient_id)
            bot.send_text_message(recipient_id, 'Okay!')

    else:
        bot.send_text_message(recipient_id, 'Thanks!')

def add_context(ContextStack, recipient_id, context):
    if recipient_id not in ContextStack:
        ContextStack[recipient_id] = []
    print(ContextStack)
    ContextStack[recipient_id].append([CONST_SAVE_MONEY,context])

def handle_user_context(ContextStack, recipient_id, response):
    last_context = ContextStack[recipient_id][-1]
    
    if (last_context[1] == CONST_MONDAY_AM_TIME) or (last_context[1] == CONST_FRIDAY_PM_TIME):
        get_time(recipient_id, last_context, response)
                
    return
    
def get_time(recipient_id, last_context, response):
    if response.isdigit():
        num = int(response)
        if (num >= 1) and (num <= 12):
            last_context.append(num)
            text = ""
            if last_context[1] == CONST_MONDAY_AM_TIME:
                text = 'Nice! Is {}AM every Monday correct? thanks!'.format(num)
            elif last_context[1] == CONST_FRIDAY_PM_TIME:
                text = 'Nice! Is {}PM every Friday correct? thanks!'.format(num)
                 
            choices = []
            for choice in [CONST_YES, CONST_NO]:
                choices.append(
                    {
                        "content_type": "text",
                        "title": choice,
                        "payload": CONST_SAVE_MONEY+"_"+CONST_TIME_CONFIRM+"_"+choice
                    }
                )
            out = quick_reply_template(text, choices)
            bot.send_message(recipient_id, out)
            return
    bot.send_text_message(recipient_id, 'Try again! Make sure to type a number (1 to 12)')

    