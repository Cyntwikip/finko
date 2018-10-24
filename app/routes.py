from app import app
from flask import Flask, request, jsonify, json, url_for, redirect, session, render_template
from app import eurekabot 
import sqlite3 as sql

ContextStack = {}
        
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
        #return 'Get request'

    elif request.method == 'POST':
        return 'Post request'

        #return redirect(url_for('predict_kaggle'))

    return '<h2>Request method type not supported</h2>' 
    
@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/api/facebook_chatbot', methods=['GET','POST'])
def finkobot():
    #print('Finko Bot')
    if request.method == 'GET':
        # print('Finko Bot GET method')
            
        # Parse the query params
        token = request.args.get('hub.verify_token')

        return eurekabot.verify_fb_token(token)
    
    elif request.method == 'POST':
        # print('Finko Bot POST method')

        #Check if there is a header
        if request.headers['Content-Type'] != 'application/json':
            print('No header')
            return 'No Json content found'

        output = request.get_json()
        print("JSON input: ", output)

        for event in output['entry']:
            if not event.get('messaging'):
                print('UNHANDLED RESPONSE!')
                break
            messaging = event['messaging']
            time_epoch = event['time']
            for message in messaging:
                recipient_id = message['sender']['id']
                
                #Check if there is a postback.payload key inside message
                #If there is, then process the postback
                if message.get('postback') and message['postback'].get('payload'):
                    postback = message['postback']['payload']
                    eurekabot.parse_postbacks(ContextStack, recipient_id, postback)

                elif message.get('message'):
                    # if user sends a quick reply
                    quick_reply = message['message'].get('quick_reply')
                    print(quick_reply)
                    if quick_reply and quick_reply.get('payload'):
                        payload = quick_reply.get('payload')
                        eurekabot.parse_quickreply(ContextStack, recipient_id, payload, time_epoch)
                        break

                    #Facebook Messenger ID for user so we know where to send response back to
                    response = message['message'].get('text')
                    if response:
                        eurekabot.parse_response(ContextStack, recipient_id, response)
                        break
                        
                    #if user sends us a GIF, photo,video, or any other non-text item
                    # attachments = message['message'].get('attachments')
                    # if attachments:
                    #     attachment = attachments[0]
                    #     attachment_type = attachment['type']
                    #     #response for send location in directions option
                    #     if attachment_type == 'location':
                    #         coordinates = attachment['payload']['coordinates']
                    #         eurekabot.directions_get_location(recipient_id, coordinates)

        return "Message Processed"

    return 'Request method type not supported'

@app.route('/api/users')
def show_users():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from users")
   
    rows = cur.fetchall()
    return render_template("users.html", rows = rows)

@app.route('/api/users/add')
def add_user():

    try:
        id = 444
        age = 22
        occupation = 'Student'
        income = 'Over 9000'

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
        #  return render_template("result.html",msg = msg)
        return msg
        con.close()
    pass

@app.route('/api/users/delete_all')
def delete_users():
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('''DELETE FROM users''')
            
            con.commit()
            msg = "Users successfully deleted in database"
    except:
        con.rollback()
        msg = "error in delete operation"
      
    finally:
        return msg
        con.close()
    pass

@app.route('/api/users/user')
def check_user():
    id = request.args.get('id')
    #print(id)
    if id:
        con = sql.connect("database.db")
        con.row_factory = sql.Row
    
        cur = con.cursor()
        cur.execute('''SELECT * FROM users WHERE id={}'''.format(id))
            
        rows = cur.fetchall()
        return 'User exists' if rows else 'User does not exist'

    else:
        return 'Use the following format: /api/users/user?id=<id>'
