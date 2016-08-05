#Tweet-o-meter: Add your own Twitter API developer keys (lines 9-12)
# and choose your own keyword/hashtag (line 56)
import time, sys
from textblob import TextBlob
from neopixel import *
from twython import TwythonStreamer

import creds

# Add Python Developer App tokens and secret keys
APP_KEY = creds.APP_KEY
APP_SECRET = creds.APP_SECRET
OAUTH_TOKEN = creds.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = creds.OAUTH_TOKEN_SECRET

# LED strip configuration:
LED_COUNT   = 60      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA     = 5       # DMA channel to use for generating signal
#LED_BRIGHTNESS = 255  # LED brightness
LED_INVERT  = False   # True to invert the signal

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
# Intialize the library (must be called once before other functions).
strip.begin()

def colorCycle():
    iterations = 0
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 255, 0))
        strip.show()

totals = {'pos':100,'neg':100,'neu':100}
colors = {'pos':(0,1,0),'neg':(1,0,0),'neu':(0,0,1)}

class MyStreamer(TwythonStreamer):
    def on_success(self,data): # When we get valid data
        if 'text' in data: # If the tweet has a text field
            tweet = data['text'].encode('utf-8')
            #print(tweet) # uncomment to display  each tweet
            tweet_pro = TextBlob(data['text']) # calculate sentiment
            # adjust value below to tune sentiment sensitivity
            if tweet_pro.sentiment.polarity > 0.05: # Positive
                print('Positive')
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(0, 255, 0))
                    strip.show()
                totals['pos']+=10
                totals['neg']-=10
                totals['neu']-=5
            # adjust value below to tune sentiment sensitivity
            elif tweet_pro.sentiment.polarity < -0.05: # Negative
                print('Negative')
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(255, 0, 0))
                    strip.show()
                totals['neg']+=10
                totals['pos']-=10
                totals['neu']-=5
            else:
                print('Neutral') # Neutral
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(0, 0, 255))
                    strip.show()
                totals['neu']+=5
                totals['pos']-=2
                totals['neg']-=2
        overall_sentiment = max(totals.keys(),key=(lambda k: totals[k]))
        print(overall_sentiment)
        for color in totals:
            if totals[color] < 10:
                totals[color] = 10
            if totals[color] > 244:
                totals[color] = 244
        r = totals['neg']
        g = totals['pos']
        b = totals['neu']
        for i in range(strip.numPixels()):
            strip.setPixelColorRGB(i, r, g, b)
            strip.show()
        print(totals)
        print('winning: ' + overall_sentiment)
        time.sleep(1.5) # Throttling
    def on_error(self, status_code, data): # Catch and display Twython errors
        print( "Error: " )
        print( status_code)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255, 255, 255))
            strip.show()

colorCycle()

for i in range(strip.numPixels()):
    strip.setPixelColorRGB(i, 0, 0, 0)
    strip.show()

#Start processing the stream
stream2 = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
while True:  #Endless loop: personalise to suit your own purposes
    try:
        stream2.statuses.filter(track='#realDonaldTrump') # <- CHANGE THIS KEYWORD!
    except KeyboardInterrupt: # Exit on ctrl-C
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
        sys.exit()
    except: # Ignore other errors and keep going
        continue
