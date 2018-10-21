from pymessenger.bot import Bot
import requests, json, random

ACCESS_TOKEN = 'EAAgxZBvF1d4cBANc3Lr1wf7nfUlnyBRAU0uASBSEzkoD2tnEyYv6mPkqHLq5MjYgydy9Npa3i0WTtLovZBEY8Avf3uJP6L0MnzZCnaQMGiuMHlsjJ3imzG2tfXG9cjbvyyJhVEHXC3eJvNsq6auxMyc8LEufEeDbuPj04kZAbFvlugghdbXg'
VERIFY_TOKEN = 'treblelab'
bot = Bot(ACCESS_TOKEN)

def get_questions():
    return {
        'Question1': {
            'question': 'In general, how would your partner or best friend describe you as a risk taker?',
            'choices': ['Real Gambler!', 'Willing to take risk only after research', 'Very cautious', 'Real risk avoider']
        }
    }

def get_name(recipient_id):
    url = "https://graph.facebook.com/{}?fields=first_name&access_token={}".format(recipient_id, ACCESS_TOKEN)
    r = requests.get(url)
    return json.loads(r.content)['first_name']

def quick_reply_template(text, choices):
    return {
        "text": text,
        "quick_replies":choices
    }

def option_init(recipient_id):
    texts = ['''Hi {}! Thank you for taking this risk assessment test'''.format(get_name(recipient_id)),
            '''Remember that risk profiles for investor changes''',
            '''You can take the test again and again to change your risk profile''']
    for text in texts:
        bot.send_text_message(recipient_id, text)

    choices = []
    for choice in ['Yes', 'No']:
        choices.append(
            {
                "content_type":"text",
                "title":choice,
                "payload":"RiskAssessmentTest_"+choice
            }
        )

    out = quick_reply_template('Would you like to take the test now?', choices)
    bot.send_message(recipient_id, out)


def parse_quickreply(recipient_id, response):
    if response[0] == 'No':
        bot.send_text_message(recipient_id, 'Got it!')
    elif response[0] == 'Yes':
        bot.send_text_message(recipient_id, "Ok, let's start!")
        choices = []
        questions = get_questions()
        key = random.choice(list(questions.keys()))
        question = questions[key]
        for choice in question['choices']:
            choices.append(
                {
                    "content_type":"text",
                    "title":choice,
                    "payload":"RiskAssessmentTest_"+key+"_"+choice
                }
            )
        
        out = quick_reply_template(question['question'], choices)
        bot.send_message(recipient_id, out)
    elif 'Question' in response[0]:
        bot.send_text_message(recipient_id, 'Your answer to {} is {}'.format(response[0], response[1]))
    else:
        bot.send_text_message(recipient_id, 'Thanks!')