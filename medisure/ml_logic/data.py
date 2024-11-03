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




def lower(text):
    try:
        return text.lower()
    except:
        return text




def eda_pipeline(df):

    print('_' * 33)
    print(f'\n\nColumns:\n{df.columns}\n\n')

    print('_' * 33)
    display(f'Total Rows: {df.shape[0]:,}') # type: ignore

    print('_' * 33)
    print('\n\nUnique data types:')
    print(df.dtypes.unique())


    print('_' * 33)
    print('\n\nDescribe the DataFrame (including categorical data):')
    print(df.describe(include='O'))

    print('_' * 33)
    print(f'\n\nNumber of duplicate rows: {df.duplicated().sum():,}')

    print('_' * 33)
    print('\n\nMissing values per column:')
    display(pd.DataFrame(df.isna().sum(), columns=['Missing Values'])) # type: ignore

    return df
