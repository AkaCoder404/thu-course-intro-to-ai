# sentiment analysis - subjective classification of text 
# experimental data comes from 4570 Sina News articles
#   2342 used to create training et
#   2228 used to create test set
# each contains at least 6 words and 1 user rating (emotion category)
#    three parts: timestamp, sentiment distribution, and text, and is divided by tab (\ t).
# each training set has (dn, cn) - (document n classifier n) 

from io import open 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from gensim import models
import pandas as pd
import jieba
import logging
import tensorflow
from tensorflow import keras
from keras import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Bidirectional,LSTM,Dense,Embedding,Dropout,Activation,Softmax 
from keras.layers import Conv2D, MaxPooling2D, Flatten, Conv1D
from keras.utils import np_utils
from keras.callbacks import Callback
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt 
import matplotlib as plotlib 
import re

# sentiment analysis - subjective classification of text 
# experimental data comes from 4570 Sina News articles
#   2342 used to create training et
#   2228 used to create test set
# each contains at least 6 words and 1 user rating (emotion category)
#    three parts: timestamp, sentiment distribution, and text, and is divided by tab (\ t).
# each training set has (dn, cn) - (document n classifier n) 

# Global Variables
classifiers_names = {0:"感动",1:"同情",2:"无聊",3:"愤怒",4:"搞笑",5:"难过",6:"新奇",7:"温馨"}
epoch_count = 5


# Parse Files
def parse(filename):
    print("parsing " + filename)
    
    totals = []
    sentimentList = [] # classifiers
    wordList = [] # bag-of-words

    with open(filename, 'r', encoding = "UTF-8") as f:
        for line in f:                  
            doc = line.split(' ', 9)                # make each line same size
            total_c = doc[0].split('Total:')[1]     # total classifiers
            sentiments = []
            for i in doc[1:8]:
                sentiments.append(float(i.split(':')[1]))
            sentiments.append(float(doc[8].split(':')[1].split('\t')[0]))
    
            doc[9] = re.sub(r"[a-zA-Z\d■:.'--'×]", "", doc[9]) # Trim For Useless numbers/characters/values
            doc[9] = re.sub(' +', ' ',doc[9]) # remove duplicate spaces
            totals.append(total_c)
            sentimentList.append(sentiments.index(max(sentiments)))
            wordList.append(doc[9])  
            
    return sentimentList, wordList
# purpose and usefulness of Word2vec is to group the vectors of similar words together 
# in vectorspace. That is, it detects similarities mathematically. Word2vec creates 
# vectors that are distributed numerical representations of word features, 
# features such as the context of individual words. 
def train_word2vec(sentences, word_vec_dimension, save_path):
    print("starting to train word vector")
    sentences_seg = []
    sen_str = "\n".join(sentences); # join all setences into one segment
    res = jieba.lcut(sen_str) # cut out stop words
    seg_str = " ".join(res)
    sen_list = seg_str.split("\n")
    for i in sen_list:
        sentences_seg.append(i.split())

    model = Word2Vec(
        sentences_seg,
        size=word_vec_dimension,        #dimension of word vector
        min_count=1,                    #word frequency threshold
        window=5                        #window size  
    )
    model.save(save_path)
    return model
# convert Chinese characters to numeric IDs through a dictionary and form a vector
def generate_id2wec(word2vec_model):
    gensim_dict = Dictionary();
    gensim_dict.doc2bow(word2vec_model.wv.vocab.keys(), allow_update=True)
    # word index, start from 1
    w2id = {
        v: k + 1 for k , v in gensim_dict.items()
    }  
    # word vector
    w2vec = {
        word: word2vec_model[word] for word in w2id.keys()
    }
    n_words = len(w2id) + 1
    embedding_weights = np.zeros((n_words, 100))
    # starting with a word with index 1 insert to numpy array 
    for w, index in w2id.items():
        embedding_weights[index, :] = w2vec[w]
    return w2id, embedding_weights
# text to indexed number 
def text_to_array(w2index, senlist):
    sentences_array = []
    for sen in senlist:
        new_sen = [ w2index.get(word,0) for word in sen]   # Word to index number
        sentences_array.append(new_sen)
    return np.array(sentences_array)
# to np arrays
def prepare_data(w2id, sentences, labels, max_len=20):
    X_train, X_val, y_train, y_val = train_test_split(sentences,labels, test_size=0.2)
    X_train = text_to_array(w2id, X_train)
    X_val = text_to_array(w2id, X_val)
    X_train = pad_sequences(X_train, maxlen=max_len)
    X_val = pad_sequences(X_val, maxlen=max_len)
    return np.array(X_train), np_utils.to_categorical(y_train) ,np.array(X_val), np_utils.to_categorical(y_val)
# define Callback function, calculate precision score,  Recall Scrore and F1-Score after each epoch
class Metrics(Callback):
    def on_train_begin(self, logs={}):
        self.val_f1s = []
        self.val_recalls = []
        self.val_precisions = []
 
    def on_epoch_end(self, epoch, logs={}): 

        val_predict = (np.asarray(self.model.predict(self.validation_data[0]))).round()
        val_targ = self.validation_data[1]

        _val_f1 = f1_score(val_targ, val_predict, average='micro')
        _val_recall = recall_score(val_targ, val_predict, average='micro')
        _val_precision = precision_score(val_targ, val_predict, average='micro')
        self.val_f1s.append(_val_f1)
        self.val_recalls.append(_val_recall)
        self.val_precisions.append(_val_precision)
   
        print("F1 Score : ",_val_f1)
        print("Precision Score : ",_val_precision)
        print("Recall Score : ",_val_recall)
  
        return 

