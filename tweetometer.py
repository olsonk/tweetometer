#Tweet-o-meter: Add your own Twitter API developer keys (lines 9-12)
# and choose your own keyword/hashtag (line 56)
import time, sys
from textblob import TextBlob
from neopixel import *
from twython import TwythonStreamer

# Add Python Developer App tokens and secret keys
APP_KEY = 'glNP0P78YpwxXpIe0GGiAxO1Y'
APP_SECRET = '4BHUxp3jyPV1gMtHMlNSYtbJlAg9YBCL3fHfvlctTKF7NFt608'
OAUTH_TOKEN = '703778980692758530-Onl4fyDNCt98Q2vayoOYnFWN9qYxcFL'
OAUTH_TOKEN_SECRET = '5YGdTvLUibo2RFTrsaZIYDJ4jvY64i7ZyBabbsRglOJdJ'

# LED strip configuration:
LED_COUNT   = 60      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA     = 5       # DMA channel to use for generating signal
#LED_BRIGHTNESS = 255  # LED brightness
LED_INVERT  = False   # True to invert the signal

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN)
# Intialize the library (must be called once before other functions).
strip.begin()

totals = {'pos':0,'neg':0,'neu':0}
colors = {'pos':(0,1,0),'neg':(1,0,0),'neu':(0,0,1)}

class MyStreamer(TwythonStreamer):
    def on_success(self,data): # When we get valid data
        if 'text' in data: # If the tweet has a text field
            tweet = data['text'].encode('utf-8')
            #print(tweet) # uncomment to display  each tweet
            tweet_pro = TextBlob(data['text']) # calculate sentiment
            # adjust value below to tune sentiment sensitivity
            if tweet_pro.sentiment.polarity > 0.1: # Positive
                print('Positive')
                strip.blink(on_time=0.4, off_time=0.2, on_color=(0, 1, 0), n=1, background=False)
                totals['pos']+=1
            # adjust value below to tune sentiment sensitivity
            elif tweet_pro.sentiment.polarity < -0.1: # Negative
                print('Negative')
                strip.blink(on_time=0.4, off_time=0.2, on_color=(1, 0, 0), n=1, background=False)
                totals['neg']+=1
            else:
                print('Neutral') # Neutral
                strip.blink(on_time=0.4, off_time=0.2, on_color=(0, 0, 1), n=1, background=False)
                totals['neu']+=1
        overall_sentiment = max(totals.keys(),key=(lambda k: totals[k]))
        for i in range(strip.numPixels()):
            strip.setPixelColor(colors[overall_sentiment])
            strip.show()
        print(totals)
        print('winning: ' + overall_sentiment)
        time.sleep(0.5) # Throttling

    def on_error(self, status_code, data): # Catch and display Twython errors
        print( "Error: " )
        print( status_code)
        strip.blink(on_time=0.5,off_time=0.5, on_color=(1,1,0),n=3)

for i in range(strip.numPixels()):
    strip.setPixelColorRGB(i, 200, 0, 150)
    strip.show()

strip.clear()

#Start processing the stream
stream2 = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
while True:  #Endless loop: personalise to suit your own purposes
    try:
        stream2.statuses.filter(track='#pokemongo') # <- CHANGE THIS KEYWORD!
    except KeyboardInterrupt: # Exit on ctrl-C
        sys.exit()
    except: # Ignore other errors and keep going
        continue
