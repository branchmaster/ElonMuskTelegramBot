from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import twint
import re

TOKEN=""
CHATID=123
oldtweetid = 123

def callbacktweet(context: CallbackContext): 
   global oldtweetid
   tweets = [] 
   #Twint configuration
   t = twint.Config() 
   t.Username = "ElonMusk"
   t.Limit = 1
   t.Filter_retweets = False
   t.Store_object = True
   t.Store_object_tweets_list = tweets
   twint.run.Search(t)
   newtweet = tweets[0]
   #check if the latest tweet it hasn't been reported yet and exclude the tweet replies @
   if(newtweet.id != oldtweetid and newtweet.tweet[0] != '@'):
      if (len(newtweet.photos) > 0): 
         #erase the link that store the photos from the tweet text
         newtweet.tweet = re.sub(r'(https:\/\/t\.co\/..........)','',newtweet.tweet) 
         if(len(newtweet.tweet) > 1): context.bot.send_message(chat_id=CHATID, text=newtweet.tweet)
         for imageurl in newtweet.photos:
            context.bot.send_photo(CHATID,imageurl)
      elif newtweet.video == 1:
         context.bot.send_message(chat_id=CHATID, text=newtweet.link)
      else:
         context.bot.send_message(chat_id=CHATID, text=newtweet.tweet) 
   oldtweetid = newtweet.id

def main():
   upd= Updater(TOKEN, use_context=True)
   job = upd.job_queue
   job.run_repeating(callbacktweet,interval=60,first=1)
   upd.start_polling()
   upd.idle()

if __name__=='__main__':
   main()
