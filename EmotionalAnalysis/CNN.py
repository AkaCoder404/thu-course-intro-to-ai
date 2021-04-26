from imports import * #contains necessary imports

class Sentiment:
    def __init__(self,w2id,embedding_weights,Embedding_dim,maxlen,classifiers):
        self.Embedding_dim = Embedding_dim
        self.embedding_weights = embedding_weights
        self.vocab = w2id
        self.classifiers = classifiers
        self.maxlen = maxlen
        self.model = self.build_model()
        
    def build_model(self):
        model = Sequential()
        model.add(Embedding(output_dim = self.Embedding_dim,
                           input_dim=len(self.vocab)+1,
                           weights=[self.embedding_weights],
                           input_length=self.maxlen))
       
        model.add(Conv1D(64, 3, padding='same'))
        model.add(Conv1D(32, 3, padding='same'))
        model.add(Conv1D(16, 3, padding='same'))
        model.add(Flatten())
        model.add(Dropout(0.2))
        model.add(Dense(180,activation='sigmoid'))    
        model.add(Dropout(0.2))
        model.add(Dense(self.classifiers,activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) 

        model.summary()
        return model

    def train(self, X_train, y_train,X_test, y_test,n_epoch=5):
        history = self.model.fit(X_train, y_train, batch_size=32, epochs=n_epoch,
                     validation_data=(X_test, y_test), callbacks=[metrics])
        self.model.save('sentiment.h5')   

        history_dict = history.history
            
        history_dict.keys()
       
        loss = history_dict['loss']
        acc = history_dict['accuracy']
        val_loss = history_dict['val_loss']
        val_acc = history_dict['val_accuracy']

        # plot accuracy
        epochs = range(1, len(acc) + 1)
        plt.plot(epochs, acc, 'bo', label='Training acc', color="red")
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy') 
        plt.legend(loc=7)
        plt.show()

    def predict(self,model_path,new_sen):
        model = self.model
        model.load_weights(model_path)
        new_sen_list = jieba.lcut(new_sen)

        while(' ' in new_sen_list) : 
            new_sen_list.remove(' ')  

        sen2id =[ self.vocab.get(word,0) for word in new_sen_list]
        sen_input = pad_sequences([sen2id], maxlen=self.maxlen)
        res = model.predict(sen_input)[0]
        return np.argmax(res)

def main():
    print("CNN Model")
    word_vec_dimension = 100
    word_max_length    = 500
    classifiers_count  = 8
    # extract data
    sentimentList_train, wordList_train = parse("sina/sinanews.train")
    sentimentList_test, wordList_test   = parse("sina/sinanews.test")
    # word 2 vector
    model = train_word2vec(wordList_train, word_vec_dimension, 'word2vec.model')
    # convert chinese characters to numeric ID through dictionary 
    w2id, embedding_weights = generate_id2wec(model)
    # convert to np array
    x_train, y_train, x_val, y_val = prepare_data(w2id, wordList_train,sentimentList_train, word_max_length)
    # create model
    senti = Sentiment(w2id,embedding_weights,word_vec_dimension,word_max_length,classifiers_count)
    
    print("starting to train")
    # train data +  validation, return results
    senti.train(x_train, y_train, x_val, y_val, 30)

    index_array = []
    pre_array = []
    label_array = []
    fout = open("CNN_out.txt", "w", encoding='utf-8')
    index = 0

    for sen_new in wordList_test:
        pre = senti.predict("./sentiment.h5",sen_new) 
        pre_array.append(pre)
        index_array.append(index)
        fout.write("{}\t{}\n".format(index, classifiers_names.get(pre)))
        label_array.append(sentimentList_test[index])
        index = index + 1

    fout.close()

    np.corrcoef(pre_array, label_array)
    plotlib.style.use('ggplot')

    plt.scatter(pre_array, label_array)
    # plt.plot(index_array, pre_array, 'bo', label='prediction')
    # plt.plot(index_array, label_array, 'b', label='label')
    plt.title('Prediction vs Found')
    plt.xlabel('Epochs')
    plt.ylabel('Prediction') 
    # plt.legend(loc=7)
    plt.show()
  
if __name__ == '__main__':
    metrics = Metrics()
    main()

