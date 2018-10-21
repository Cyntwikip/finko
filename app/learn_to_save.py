from pymessenger.bot import Bot

ACCESS_TOKEN = 'EAAgxZBvF1d4cBANc3Lr1wf7nfUlnyBRAU0uASBSEzkoD2tnEyYv6mPkqHLq5MjYgydy9Npa3i0WTtLovZBEY8Avf3uJP6L0MnzZCnaQMGiuMHlsjJ3imzG2tfXG9cjbvyyJhVEHXC3eJvNsq6auxMyc8LEufEeDbuPj04kZAbFvlugghdbXg'
VERIFY_TOKEN = 'treblelab'
bot = Bot(ACCESS_TOKEN)

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
    for choice in ['Yes', 'No']:
        choices.append(
            {
                "content_type":"text",
                "title":choice,
                "payload":"LearnToSave_"+choice
            }
        )
        
    out = quick_reply_template('Do you want me to remind you to save on a weekly basis?', choices)
    bot.send_message(recipient_id, out)


def parse_quickreply(recipient_id, response):
    if response[0] == 'No':
        bot.send_text_message(recipient_id, 'Got it!')
    elif response[0] == 'Yes':
        text = 'Got it! When do you want me to remind you? Salamat'
        choices = []
        for choice in ['Every Monday AM', 'Every Friday PM']:
            choices.append(
                {
                    "content_type":"text",
                    "title":choice,
                    "payload":"LearnToSave_Day_"+choice
                }
            )
        out = quick_reply_template(text, choices)
        bot.send_message(recipient_id, out)
    elif response[0] == 'Day':
        bot.send_text_message(recipient_id, 'You have selected '+response[1])
    else:
        bot.send_text_message(recipient_id, 'Thanks!')