from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import twint
#import nest_asyncio
import random
import re
import requests
import shutil
import time
import datetime
#quotefile = open('quotes.txt','r')
#linelist = quotefile.read().split('\n') 
#quotefile.close()

TOKEN=""

def mining(update,context): 
   oldtweetid = 1
   tweets = [] 
   #Twint configuration
   t = twint.Config() 
   t.Username = "ElonMusk"
   t.Limit = 1
   t.Filter_retweets = False
   t.Store_object = True
   
  
   while True:
      time.sleep(10)
      tweets = []
      t.Store_object_tweets_list = tweets
      twint.run.Search(t)
      newtweet = tweets[0]

      #check if the latest tweet it hasn't been reported yet and exclude the tweet replies @
      if(newtweet.id != oldtweetid and newtweet.tweet[0] != '@'):
         if (len(newtweet.photos) > 1): 
            #erase the link that store the photos from the text
            newtweet.tweet = re.sub(r'(https:\/\/t\.co\/..........)','',newtweet.tweet) 
            if(len(newtweet.tweet) > 1): context.bot.send_message(chat_id=update.effective_chat.id, text=newtweet.tweet)
            for imageurl in newtweet.photos:
               context.bot.send_photo(update.effective_chat.id,imageurl)
         elif newtweet.video == 1:
            context.bot.send_message(chat_id=update.effective_chat.id, text=newtweet.link)
         else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=newtweet.tweet) 
      oldtweetid = newtweet.id
   
def main():
   upd= Updater(TOKEN, use_context=True)
   disp=upd.dispatcher
   disp.add_handler(CommandHandler("mining", mining))
   upd.start_polling()
   upd.idle()

if __name__=='__main__':
   main()
