import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')



def clean_text(text):

    text = text.lower()

    text = text.translate(str.maketrans('', '', string.punctuation))

    text = re.sub(r'\d+', '', text)

    # stop_words = set(stopwords.words('english'))
    # words = nltk.word_tokenize(text)
    # filtered_words = [word for word in words if word not in stop_words]

    # lemmatizer = WordNetLemmatizer()
    # lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    # return ' '.join(lemmatized_words)
    return text
