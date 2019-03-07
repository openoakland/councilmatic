
#   Post a message to twitter

import os
import sys
import twitter
import datetime


'''
This runs off a a file  ".tweeter"  which resides in your home directory.  The format is below

    consumer_key: "consumer_key"
    consumer_secret: "consumer_password"
    access_key: "access_key"
    access_secret: "access_password"
    
Make sure this file does not have world access and is not accessible to the public    
'''


def read_dot_tweeter():  # Read the .tweeter file in the home directory to get the keys to the twitter account
    path = os.path.expanduser('~') + "/.tweeter"
    file = open(path, "r")
    key = []
    for i in range(0, 4):
        line = file.readline().split()
        key.append(line[1])
    print(key)
    return key


# Main Program

encoding = None
key = read_dot_tweeter()  # Fetch the code values from  ~.tweeter
consumer_key = key[0]
consumer_secret = key[1]
access_key =  key[2]
access_secret = key[3]

message = "Tweeting for Councilmatic - " + str(datetime.datetime.now())

if not consumer_key or not consumer_secret or not access_key or not access_secret:
    print("To Tweet, you need four environmental variables")
    sys.exit(2)
api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                  access_token_key=access_key, access_token_secret=access_secret,
                  input_encoding=encoding)
try:
    status = api.PostUpdate(message)
except UnicodeDecodeError:
    print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
    print("Try explicitly specifying the encoding with the --encoding flag")
    sys.exit(2)

print("{0} just posted: {1}".format(status.user.name, status.text))


