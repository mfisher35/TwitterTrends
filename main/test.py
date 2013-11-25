import re
import string 
a = "a i like http://shit.com"
pieces = a.split()
new_tweet = ""

for word in pieces:
  if "http://" in word:
   new_url = '<a href="' + word +'">' + word + "</a>"
   print new_url
   new_tweet = string.replace(a,word,new_url)

print new_tweet

