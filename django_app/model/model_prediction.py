import re
import pickle
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
import numpy as np
from bs4 import BeautifulSoup
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer


stopwords_list = nltk.corpus.stopwords.words("english")
le = nltk.stem.WordNetLemmatizer()
with open('model/imdb_vocab.txt', 'r', encoding='utf8') as f:
  vocab = f.read().splitlines()

vect_model_bag = TfidfVectorizer(vocabulary=vocab, max_df=0.8, min_df=4)

models_machine = []
with open("model/machine_models_score.pckl", "rb") as f:
  while True:
    try:
      models_machine.append(pickle.load(f))
    except EOFError: break
    
def get_vectors(text):
  tokens = BeautifulSoup(text, "lxml").get_text()
  tokens = re.sub('[^a-zA-Z]', ' ', tokens.lower().strip()).split()
  tokens = [le.lemmatize(word) for word in tokens if word not in stopwords_list and len(word) > 3]
  vectors_bag = vect_model_bag.fit_transform([' '.join(tokens)])
  return vectors_bag

def get_machine_prediction(vectors):
  predictions = []
  for model in models_machine:
    prediction = float(model.predict(vectors))
    prediction = 1 if prediction < 1 else (10 if prediction > 10 else prediction)
    predictions.append(prediction)
  return predictions

def count_score(predictions):
  score = np.round(np.median(predictions, axis=0), 1)
  score_fract = score - np.floor(score)
  if score_fract > 0.3 and score_fract < 0.8:
    score = np.floor(score) + 0.5
  else:
    score = np.round(score).astype(int)
  return score