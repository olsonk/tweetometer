#Tweet-o-meter: Add your own Twitter API developer keys (lines 9-12)
# and choose your own keyword/hashtag (line 56)
import time, sys
from textblob import TextBlob
from gpiozero import RGBLED
from twython import TwythonStreamer

# Add Python Developer App tokens and secret keys
APP_KEY ='ENTER APP KEY HERE' # <- CHANGE
APP_SECRET = 'ENTER APP SECRET HERE' # <- CHANGE
OAUTH_TOKEN = 'ENTER OAUTH_TOKEN HERE' # <- CHANGE
OAUTH_TOKEN_SECRET = 'ENTER OAUTH_TOKEN_SECRET HERE' # <- CHANGE

# Set our RGB LED pins
status_led = RGBLED(14,15,18, active_high=True)
# Set active_high to False for common anode RGB LED
status_led.off()
totals = {'pos':0,'neg':0,'neu':0}
colours = {'pos':(0,1,0),'neg':(1,0,0),'neu':(0,0,1)}

class MyStreamer(TwythonStreamer):
    def on_success(self,data): # When we get valid data
        if 'text' in data: # If the tweet has a text field
            tweet = data['text'].encode('utf-8')
            #print(tweet) # uncomment to display  each tweet
            tweet_pro = TextBlob(data['text']) # calculate sentiment
            # adjust value below to tune sentiment sensitivity
            if tweet_pro.sentiment.polarity > 0.1: # Positive
                print('Positive')
                status_led.blink(on_time=0.4, off_time=0.2, on_color=(0, 1, 0), n=1, background=False)
                totals['pos']+=1
            # adjust value below to tune sentiment sensitivity
            elif tweet_pro.sentiment.polarity < -0.1: # Negative
                print('Negative')
                status_led.blink(on_time=0.4, off_time=0.2, on_color=(1, 0, 0), n=1, background=False)
                totals['neg']+=1
            else:
                print('Neutral') # Neutral
                status_led.blink(on_time=0.4, off_time=0.2, on_color=(0, 0, 1), n=1, background=False)
                totals['neu']+=1
        overall_sentiment = max(totals.keys(),key=(lambda k: totals[k]))
        status_led.color = colours[overall_sentiment]
        print(totals)
        print('winning: ' + overall_sentiment)
        time.sleep(0.5) # Throttling

    def on_error(self, status_code, data): # Catch and display Twython errors
        print( "Error: " )
        print( status_code)
        status_led.blink(on_time=0.5,off_time=0.5, on_color=(1,1,0),n=3)

#Start processing the stream
stream2 = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
while True:  #Endless loop: personalise to suit your own purposes
    try:
        stream2.statuses.filter(track='magpi') # <- CHANGE THIS KEYWORD!
    except KeyboardInterrupt: # Exit on ctrl-C
        sys.exit()
    except: # Ignore other errors and keep going
        continue
