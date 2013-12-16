# Create your views here.
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from alchemyapi import AlchemyAPI
import re
import twitter
import time
import pickle
import string
import cgi 

GETNEWTWEETS = 0
NUM_STATUSES = 200
MIN_RETWEETS = 200
MAXTWEETS = 999999
filename = 'TOPTWEETS.adb'
ONTHEFLY = False


def clean(n):
  new = []
  for char in n:
    if re.match('^[\w-]+$',char) is not None:
     new.extend(char)
    elif " " in char:
     new.extend(char)
    elif "'" in char:
     new.extend(char)
  return string.join(new,"")


def index(request):

  alchemyapi = AlchemyAPI()
  template = loader.get_template('main/index.html')

 
  api = twitter.Api(consumer_key='CCC',consumer_secret='SSS', access_token_key='AAA', access_token_secret='TTT')

  infile = open(filename,'r')
  statuses = pickle.load(infile) 
  statuses2 = []
  if GETNEWTWEETS:
   statuses2 = api.GetHomeTimeline(NUM_STATUSES)
 
  countclash = 0
  countpass = 0
  passt = 0
 
  if not ONTHEFLY: 
   for item in statuses2:
     passt = 1
     for fitem in statuses:
       if fitem.id == item.id:
         countclash = countclash + 1
         passt = 0
     if passt > 0:
         temp = clean(item.text)
         response = alchemyapi.category('text',temp)
         category = "unknown"
         if response['status'] == 'OK':
           category = response['category']
           cat_score = response['score']
         else:
           print('Error in entity extraction call: ', response['statusInfo'])
         item.lang = category
         statuses.append(item)
         countpass = countpass + 1       
   
  #print("%i clash %i pass" % (countclash,countpass))
   
  ai = -1
  bi = -1
  
  size = len(statuses)
   
  for a in statuses:
   ai = ai + 1
  
   cmax = a.retweet_count
   cmaxindex = ai
  
   for bi in range(ai,size):
      if statuses[bi].retweet_count > cmax:
       cmaxindex = bi
       cmax = statuses[bi].retweet_count
  
   if cmaxindex != ai:    
     statuses[ai], statuses[cmaxindex] = statuses[cmaxindex], statuses[ai]
  
  tweet_list = []
  index = 0
 
  for s in statuses:
   if index < MAXTWEETS:
    if s.retweet_count > MIN_RETWEETS: 
     tweet_list.append(s) 
     index = index + 1
  
  
  newsize = len(statuses)
 
  if not ONTHEFLY: 
#   del statuses[NUM_STATUSES:newsize]
   f = open(filename,'w')
   pickle.dump(statuses, f)
     

  context = RequestContext(request, {'tweet_list' : tweet_list})
  return HttpResponse(template.render(context))  


def filtered(request, filter_id):


#  api = twitter.Api(consumer_key='4GwbDHXzYqgu2lRWMibqGA',consumer_secret='OU5eohHs3g6xGXzEncTW3HZQqlNDLPWx2KJCqvK7U', access_token_key='1951946809-FP6FDYLeT26apHIYGOkYEQZOBt1GTa1EA2HGyFA', access_token_secret='89c8mjSPzARbZ74KrTA5648JI1R3apkfqsw32K6Fg')
  
  infile = open(filename,'r')
  ostatuses = pickle.load(infile)
  
  
  statuses = []

  countclash = 0
  countpass = 0
  passt = 0
 
  if not ONTHEFLY: 
   for oitem in ostatuses:
     passt = 1
     for item in statuses:
       if oitem.id == item.id:
         countclash = countclash + 1
         passt = 0
     if passt > 0:
         statuses.append(oitem)
         countpass = countpass + 1       
   
#  print("%i clash %i pass" % (countclash,countpass))
   
  ai = -1
  bi = -1
  
  size = len(statuses)
   
  for a in statuses:
   ai = ai + 1
  
   cmax = a.retweet_count
   cmaxindex = ai
  
   for bi in range(ai,size):
      if statuses[bi].retweet_count > cmax:
       cmaxindex = bi
       cmax = statuses[bi].retweet_count
  
   if cmaxindex != ai:    
     statuses[ai], statuses[cmaxindex] = statuses[cmaxindex], statuses[ai]
  
  tweet_list = []
  index = 0
  cats = ["culture_politics","gaming","religion","business","computer_internet","science_technology","sports","recreation","health","arts_entertainment","weather","law_crime","other"]
  cats2 = ["Culture And Politics","Gaming","Religion","Business","Computers And Internet","Science And Technology","Sports","Recreation","Health","Arts And Entertainment","Weather","Law And Crime","All"]
  cat_no = [0,1,2,3,4,5,6,7,8,9,10,11,12]

  for s in statuses:
   if index < MAXTWEETS:
    if s.retweet_count > MIN_RETWEETS:
      if s.lang in cats[int(filter_id)]: 
        tweet_list.append(s) 
        index = index + 1
      elif int(filter_id) > 11:
        tweet_list.append(s)
  
  newsize = len(statuses)
 
#  if not ONTHEFLY: 
#   del statuses[NUM_STATUSES:newsize]
#   f = open(filename,'w')
   
#   pickle.dump(statuses, f)

  category2 = cats2[int(filter_id)]
  return render(request, 'main/filter.html', {'tweet_list' : tweet_list, 'category' : category2}) 
