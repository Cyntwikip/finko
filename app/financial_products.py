from pymessenger.bot import Bot
import requests, json, random

ACCESS_TOKEN = 'EAAgxZBvF1d4cBANc3Lr1wf7nfUlnyBRAU0uASBSEzkoD2tnEyYv6mPkqHLq5MjYgydy9Npa3i0WTtLovZBEY8Avf3uJP6L0MnzZCnaQMGiuMHlsjJ3imzG2tfXG9cjbvyyJhVEHXC3eJvNsq6auxMyc8LEufEeDbuPj04kZAbFvlugghdbXg'
VERIFY_TOKEN = 'treblelab'
bot = Bot(ACCESS_TOKEN)

### Context
CONST_LEARN_MORE = 'Learn More'
CONST_NEWS_LINKS = 'News Links'
CONST_RECOMMENDED_INVESTMENTS = 'Recommended Investments'
CONST_LEARN_MORE_STOCKS = 'Learn more about stocks'
CONST_NEWS_LINKS_STOCKS = 'News Links about stocks'
CONST_RECOMMENDED_STOCKS = 'See recommendations'
CONST_YES = 'Yes'
CONST_NO = 'No'

###

def get_questions():
    return {
        'Question_1': {
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

def generic_template(title, img, buttons):
    return {
        "title":"Welcome!",
        "image_url":img,
        # "subtitle":"We have the right hat for everyone.",
        "buttons": buttons
    }
    pass

def option_init(recipient_id):

    texts = ['''Glad to know that you are willing to learn about financial instruments!''',
             '''So what do you want to learn?''']
    for text in texts:
        bot.send_text_message(recipient_id, text)

    carousel = []

    # Carousel 1
    buttons = []
    for choice in [CONST_LEARN_MORE, CONST_NEWS_LINKS, CONST_RECOMMENDED_INVESTMENTS]:
        buttons.append(
            {
                "type":"postback",
                "title":choice,
                "payload":"FinancialProducts_"+choice
            }
        )
    carousel.append(generic_template('Mutual Funds', './static/img/finko/img1.jpg', buttons))

    # Carousel 2
    buttons = []
    for choice in [CONST_LEARN_MORE_STOCKS, CONST_NEWS_LINKS_STOCKS, CONST_RECOMMENDED_STOCKS]:
        buttons.append(
            {
                "type":"postback",
                "title":choice,
                "payload":"FinancialProducts_"+choice
            }
        )
    carousel.append(generic_template('Stocks', './static/img/finko/img2.jpg', buttons))

    bot.send_generic_message(recipient_id, carousel)

def parse_quickreply(recipient_id, response):
    pass