from pymessenger.bot import Bot
import requests, json, random, time

ACCESS_TOKEN = 'EAAgxZBvF1d4cBANc3Lr1wf7nfUlnyBRAU0uASBSEzkoD2tnEyYv6mPkqHLq5MjYgydy9Npa3i0WTtLovZBEY8Avf3uJP6L0MnzZCnaQMGiuMHlsjJ3imzG2tfXG9cjbvyyJhVEHXC3eJvNsq6auxMyc8LEufEeDbuPj04kZAbFvlugghdbXg'
VERIFY_TOKEN = 'treblelab'
bot = Bot(ACCESS_TOKEN)

### Constants
CONST_LEARN_MONEY = 'LearnMoney'
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
        "title": title,
        "image_url": img,
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
                "type": "postback",
                "title": choice,
                "payload": CONST_LEARN_MONEY+"_"+choice
            }
        )
    img_url = './static/img/finko/img2.jpg'
    img_url = "https://treblelab-finko.herokuapp.com/static/img/finko/img1.jpg"
    carousel.append(generic_template('Mutual Funds', img_url, buttons))

    # Carousel 2
    buttons = []
    for choice in [CONST_LEARN_MORE_STOCKS, CONST_NEWS_LINKS_STOCKS, CONST_RECOMMENDED_STOCKS]:
        buttons.append(
            {
                "type": "postback",
                "title": choice,
                "payload": CONST_LEARN_MONEY+"_"+choice
            }
        )
    img_url = "https://treblelab-finko.herokuapp.com/static/img/finko/img2.jpg"
    carousel.append(generic_template('Stocks', img_url, buttons))

    bot.send_generic_message(recipient_id, carousel)

def parse_quickreply(recipient_id, response):
    pass

def parse_postbacks(ContextStack, recipient_id, postback):
    '''
    Parses the postback event that was triggered.
    '''

    postback_splitted = postback.split('_')

    if postback_splitted[1] == CONST_LEARN_MORE:
        texts = ['''We always hear news about the mutual funds, but what is it really?''',
                 '''Mutual fund is a pool of money from individual or corporate investors''',
                 '''This is then invested in different financial securities''',
                 '''Examples of these are stocks, bonds or money market instruments''',
                 '''The value of a share of mutual fund is called Net Asset Value''',
                 '''It is calculated by dividing the total fund's value with the total number of outstanding shares''',
                 '''Please note that the funds are managed by a professional fund manager''',
                 '''So what are the benefits of investing in mutual funds''',
                 '''First, you don't need large amount of money before you can invest in a mutual fund''',
                 '''Second, transaction costs for mutual funds are lower''',
                 '''This is because it is bought in bulk or 'maramihan' ''',
                 '''Third, it is a combination of different investments from stocks, bonds, and money market instruments''',
                 '''This will spread the risk of the stocks, making the mutual fund a lower risk invesment''',
                 '''Fourth, you can invest easily in mutual funds as it is managed by a professional fund manager''',
                 '''That's all about Mutual Funds for now!''',
                #  '''Do you want to learn about other financial instruments? or do you want to know mutual funds that fit your profile?'''
                 ]
        for text in texts:
            bot.send_text_message(recipient_id, text)
            time.sleep(0.5)
    else:
        bot.send_text_message(recipient_id, 'Feature to be implemented in the future.')
    return