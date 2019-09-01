#!/usr/bin/env python
"""mailsend: A tool for sending notifications to ourselves, from anywhere with an internet connection."""
__version__ = "0.1.0"
__author__ = "Sonny Kothapally (me@sonnyksimon.com)"
__copyright__ = "(C) 2019 pancubs. BSD 2-Clause."
__contributors__ = []

from flask import Flask, request
from flask_mail import Mail, Message
import os
import datetime

##utils
def httpdate(date_obj):
    """
    Formats a datetime object for use in HTTP headers.
        >>> import datetime
        >>> httpdate(datetime.datetime(1970, 1, 1, 1, 1, 1))
        'Thu, 01 Jan 1970 01:01:01 GMT'
    """
    return date_obj.strftime("%a, %d %b %Y %H:%M:%S GMT")

def parsehttpdate(string_):
    """
    Parses an HTTP date into a datetime object.
        >>> parsehttpdate('Thu, 01 Jan 1970 01:01:01 GMT')
        datetime.datetime(1970, 1, 1, 1, 1, 1)
    """
    try:
        t = time.strptime(string_, "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        return None
    return datetime.datetime(*t[:6])

##main
app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": os.environ.get('MAIL_SERVER'),
    "MAIL_PORT": os.environ.get('MAIL_PORT', 465),
    "MAIL_USE_TLS": os.environ.get('MAIL_USER_TLS', False),
    "MAIL_USE_SSL": os.environ.get('MAIL_USE_SSL', True),
    "MAIL_USERNAME": os.environ.get('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.environ.get('MAIL_PASSWORD')
}

app.config.update(mail_settings)
mail = Mail(app)

@app.route('/')
def index():
    return "You can send mail via /send/. You need to send a HTTP POST request with: `authkey`, `subject`, `recipient` and `body`."

""" Uncomment for testing
@app.route('/send-mail/')
def send_mail():
    try:
        msg = Message("Send Mail Tutorial!",
            sender=os.environ.get('MAIL_USERNAME'),
            recipients=["sonnyksimon@gmail.com"])
        msg.body = "Yo!\nHave you heard the good word of Python???"           
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return(str(e)) """

@app.route('/send/', methods=['POST'])
def send():
    """ Sends notifications via Flask-Mail. """
    try:
        data = request.get_json()
        if data['authkey'] != os.environ.get('MAIL_AUTHKEY'): 
            return "Ooops. Wrong `authkey`."
        msg = Message(data['subject'],
            sender=os.environ.get('MAIL_USERNAME'),
            recipients=[data['recipient']])
        msg.body = data['body']           
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        print('We got an error at ' + httpdate(datetime.datetime.now()))
        print(str(e)) 
        return 'There was an error with that request.'

if __name__ == '__main__':
    app.run()
