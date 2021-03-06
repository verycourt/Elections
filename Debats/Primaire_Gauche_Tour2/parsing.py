from xml.etree import cElementTree as ET
import re
from collections import Counter
import unicodedata
import nltk
from nltk import word_tokenize
import string
from nltk.corpus import stopwords
from stop_words import get_stop_words
from pytagcloud import create_tag_image, make_tags
import time



def tokenize(s):
    return word_tokenize(s.lower())

stop2 = get_stop_words('fr')
print(stop2)
french_stopwords = set(stopwords.words('french'))
custom_stops = ['rt']

def count_word(corpus):
	word_list = list()

	tokens = tokenize(corpus)

	tokens_n = [token for token in tokens if token not in french_stopwords
					and token  not in string.punctuation and token not in stop2]
#		print("Document " + str(i) + " /" + str(nb_tweet))

	return tokens_n



####################################################################################
####################################################################################




link = 'C:\\Users\\Mohamed\\MS BGD\\fil_rouge_lepoint\\débat\\transcription_text_debat4.xml'

tree = ET.parse('C:\\Users\\Mohamed\\MS BGD\\fil_rouge_lepoint\\débat\\transcription_text_debat4.xml')
root = tree.getroot()

result = ''
for element in root.iter():
    try :
        result += element.text + ' '
    except:
        continue

result = result.replace("\n", "").replace("'", " ").replace("...", "")
print(result.count("- M. Valls :"))
print(result.count("- B. Hamon :"))

textValls = ""
textHamon = ""

resTemp = result

for i in range(result.count("- M. Valls :")) :
    start = result.find('- M. Valls :') + 12
    end = result.find('- ', start)
    textValls += result[start:end]
    result = result[end:]

result = resTemp
for i in range(result.count("- B. Hamon :")) :
    start = result.find('- B. Hamon :') + 12
    end = result.find('- ', start)
    textHamon += result[start:end]
    result = result[end:]


word_list_hamon = count_word(textHamon)
count_hamon = Counter(word_list_hamon)
nb = count_hamon["aujourd"]
del count_hamon["aujourd"]
del count_hamon["hui"]
count_hamon["aujourd'hui"] = nb

word_list_valls = count_word(textValls)
count_valls = Counter(word_list_valls)
nb = count_valls["aujourd"]
del count_valls["aujourd"]
del count_valls["hui"]
count_valls["aujourd'hui"] = nb

TAG_PADDING = 0.3
ECCENTRICITY = 0.1
tags = make_tags(count_hamon.most_common(75), maxsize=75)
create_tag_image(tags,'hamon_cloud.png', layout=2, size=(700,400),  fontname='Philosopher', rectangular=False)
tags = make_tags(count_valls.most_common(75), maxsize=100)
create_tag_image(tags,'valls_cloud.png',layout=2, size=(700,400),  fontname='Philosopher', rectangular=False)

help(create_tag_image)
