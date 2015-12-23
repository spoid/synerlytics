import tweepy
import spacy.en
from spacy.parts_of_speech import VERB, NOUN, ADJ, ADV
import time
import random
import numpy as np
#import sys 
#sys.setdefaultencoding('utf-8')



def generate_tweet(nouns,verbs,adjectives,adverbs):
    print "--------"
    
    dice = np.random.randint(1,100)
    text = ""
    
    if dice > 30:
        adverb = random.choice(adverbs.keys())
        #print adverb
        text = text + adverb + " "
    
    text = text + random.choice(verbs.keys()) + " "
    
    text = text + random.choice(adjectives.keys()) + " "
    
    #dice = np.random.randint(1,100)
    #if dice > 80:
    #    text = text + "and " + random.choice(adjectives.keys()) + " "
        
    dice = np.random.randint(1,100)
    if dice < 70:
        #PLURAL NON-END NOUN
        while True:
            current_noun = random.choice(nouns.keys())
            if "PRENOUN" not in nouns[current_noun]:
                final_noun = current_noun
                if "NOPL" not in nouns[current_noun]:
                    if current_noun[-1:] == "y":
                        final_noun = final_noun[:-1]+"ie"
                    final_noun = final_noun + "s"
                text = text + final_noun
                break
    else:
        #SINGULAR ANYNOUN 
        text = text + random.choice(nouns.keys()) + " "
        
        #+ PLURAL NON-END NOUN
        while True:
            current_noun = random.choice(nouns.keys())
            if "PRENOUN" not in nouns[current_noun]:
                final_noun = current_noun
                if "NOPL" not in nouns[current_noun]:
                    if current_noun[-1:] == "y":
                        final_noun = final_noun[:-1]+"ie"
                    final_noun = final_noun + "s"
                text = text + final_noun
                break
    
    #advanced: check for no duplicates 
    
    return text




##LOGIN TWITTER

CONSUMER_KEY ="kW5p349xO3DSeXvi5JaMBPWqc"
CONSUMER_SECRET = "L1zbyQBidiBlBCioaSP2jW5bxE11OxX9vMSuDm5qAr3RNXuV6l"   
ACCESS_KEY = "4560519855-NtnYFamEHZam46ExDca74AxqWK21FmFiNdDmGAN"    
ACCESS_SECRET = "iwqnkjXAk9pLDjS2oMzf2sTggbuh9omjWOPc8QmLNsHTk"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)





#INITIALIZE WORD TXT STUFF

with open("buzzwords") as f:
    data = f.readlines()
    
    
#get nouns
nouns = {}

for entry in data:
    print entry
    word = entry.split("|")[0].rstrip()
    pos = entry.split("|")[1].rstrip()
    if word.lower() not in nouns and "NOUN" in pos:
        print word.lower()
        nouns[word.lower().decode('utf-8')] = pos
for noun in nouns:
    print noun

###PRE-NOUN HANDLING




#get verbs
#+ing oder VX
verbs = {}

for entry in data:
    print entry
    word = entry.split("|")[0].rstrip()
    pos = entry.split("|")[1].rstrip()
    
    if word.lower() not in verbs and " V" in pos and not "VX" in pos:
        #if it ends with e, cut e
        if word[-1:] == "e":
            word = word[:-1]
        verbs[(word.lower()+"ing").decode('utf-8')] = pos
    if word.lower() not in verbs and " V" in pos and "VX" in pos:
        verbs[word.lower().decode('utf-8')] = pos  
#for verb in verbs:
#    print verb




#get adjectives
#ADJ
#ADJV
#VERB + e/d
adjectives = {}

for entry in data:
    print entry
    word = entry.split("|")[0].rstrip()
    pos = entry.split("|")[1].rstrip()
    if word.lower() not in adjectives and ("ADJ" in pos or "ADXX" in pos):
        adjectives[word.lower().decode('utf-8')] = pos
for adjective in adjectives:
    print adjective 





#get adverbs
#ADV
#ADJV + ly
adverbs = {}

for entry in data:
    print entry
    word = entry.split("|")[0].rstrip()
    pos = entry.split("|")[1].rstrip()
    if word.lower() not in adverbs and "ADV" in pos:
        adverbs[word.lower().decode('utf-8')] = pos
    if word.lower() not in adverbs and "ADXX" in pos:
        #if ends with le, remove le
        if word[-2:] == "le":
            word = word[:-2]
        adverbs[(word.lower()+"ly").decode('utf-8')] = pos
for adverb in adverbs:
    print adverb



while True:
    business_tweet = generate_tweet(nouns, verbs, adjectives, adverbs)

    api.update_status(business_tweet)
    print "tweeted: ", business_tweet
    
    time.sleep(np.random.randint(66,333))


