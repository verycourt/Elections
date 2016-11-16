import nltk as NL
import pandas as pd
import normalizr as nm
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords


df = pd.read_csv("output_got.csv", error_bad_lines = False, sep = ";")
# Normalise Text datas in french
norm = nm.Normalizr(language = 'fr')
df['text'] = df['text'].apply(norm.normalize)

print(df['text'].ix[1])
# Remove stop words
stop = set(stopwords.words('french'))
df['text'] = df['text'].apply(lambda X : str.lower(X) if X not in stop else '')
print(df['text'].ix[1])

# Tokenisation of Text
tokenizer = TreebankWordTokenizer()
df['tokens'] = df['text'].apply(tokenizer.tokenize)
print(df['tokens'].head(10))