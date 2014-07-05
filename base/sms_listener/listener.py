#
#SMS test via Google Voice
#
#John Nagle
#   nagle@animats.com
#
from googlevoice import Voice
import sys
import urllib
import urllib2
import BeautifulSoup
import time


def extractsms(htmlsms) :
    """
    extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []										# accum message items here
    #	Extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)			# parse HTML into tree
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations :
        #	For each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in rows :								# for all rows
            #	For each row, which is one message, extract all the fields.
            msgitem = {"id" : conversation["id"]}		# tag this message with conversation ID
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans :							# for all spans in row
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()	# put text in dict
            msgitems.append(msgitem)					# add msg dictionary to list
    return msgitems
    
voice = Voice()
voice.login(email="smsfinancetracker@gmail.com", passwd="i=sqrt-1")

while True:
    voice.sms()
    for msg in extractsms(voice.sms.html):
        text = msg['text']
        print "Text " + text
        account_tag = str(text[0 : text.index(' ')]).upper()
        print "Account Tag: " + account_tag
        text = text[text.index(' ') + 1: ]
        amount = text[0 : text.index(' ')]
        print "Amount: " + amount
        text = text[text.index(' ') + 1: ]
        comment = text
        print "Comment: " + comment
        phone_number = msg['from'][-11:-1]
        print "From " + phone_number
        
        url = 'http://127.0.0.1:8000/sms_update/'
        values = {'phone_number' : phone_number,
                  'amount' : amount,
                  'account_tag' : account_tag,
                  'comment' : comment}
        
        try:
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            the_page = response.read()
            print the_page
        except urllib2.HTTPError, e:
            print e.fp.read()
    for message in voice.sms().messages:
        message.delete()
    
    time.sleep(60)
#end while