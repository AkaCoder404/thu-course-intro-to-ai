# 情感分析 Sentiment Analysis

人工智能的第三个试验

## Abstract
Sentiment Analysis allows users to gain an overview of public opinion behind certain topics. Using concepts such as natural language processing, text analysis, computational linguistics, and biometrics allows to identify, extract, and study affective states and subjective information’s.  The goal of this experiment was to determine the “主管因素” expressed by the author. 

These two python programs, CNN.py and LSTM.py uses TensorFlow backend (Keras implementation)  to produce a model capable of predicting the sentiment polarity associated with Sina news article. This programming experiment implements and trains two models, the Convulational Neural Network (CNN) and Recurrent Neural Network (RNN) , to complete the sentiment analysis on all the articles. The RNN model is modified to use the Long Short-Term Memory (LSTM) architecture. 

The corpora, or experimental data comes from a total of 4570 Sina News articles. Out of the 4570, 2342 is used to create the training set, which comes from sina/sinanews.train, and the other 2228 is used to create the test set, which comes from 2228. The versions of the libraries used are TensorFlow 2.0.0 and Keras 2.3.1. Since I ran the code on Windows, I have also configured it to run on GPU using the tensorflow-gpu, using the CUDA Toolkit. Some other system requirements are listed at the end.

## Implementation

The implementation process of both models is same:
1.  Import the training text data and test text data sets from sinanews.train and sinanews.test using the parse function, removing all unnecessary characters (such as punctuation and letters). 
2.	Use jieba to cut out all “stop words” , create a dictionary of the data from the Word2Vec model, starting with the index 1, and define the model using the train_word2vec function. 
3.	Convert Chinese characters to numeric IDs through diction and form a vector.
4.	Define the model.
5.	Train the model.
6.	Define callback function, calculate the precisions core, recall score, and F1 score after each epoch defined in Metrics.
7.	Sketch the accuracy vs. epoch curve for training and validation after each the model is full trained defined in Sentiment.
8.	Perform sentiment analysis using the trained model on the test text dataset sinanews.test.
9.	Calculate the correlation coefficient and draw the result distribution map.
Since both implementations’ processes are similar, shared import libraries and functions are listed in the imports.py.  Differences in model design are shown in their respective python files. 

CNN: 
We first truncate each line from sinanews so that they are all the same size, removing all stop words and unnecessary characters.  Then we use the embedding layer to convert each word encoding into a word vector. As this process is memory intensive, a warning is given. “UserWarning: Converting sparse IndexedSlices to a dense Tensor of unknown shape. This may consume a large amount of memory. "Converting sparse IndexedSlices to a dense Tensor of unknown shape.”  We then split the training data into a training set and a validation set, with a 4:1 ratio. Then we build the model with Convulation1D kernals, with sigmoid as the activation function and loss using a logarithmic loss function.  After the model is done fitting multiple times (epoch = 30). We then display the graph using pyplot. After, we perform sentiment analysis on the test entries and plot the distribution of the sentiment for predicted vs found for the results.

LSTM: 
This modified version of a recurrent neural network is implemented in the same way as the CNN script, with the exception of the model itself. 



## Experimental Results
The experimental results can be found in the results folder. 

- CNN_graph: graphs the accuracy vs epoch and validation vs epoch during the training process of CNN. 
- CNN_distribution: graphs the sentiment analysis distribution for predicted vs found during the testing process of CNN.
- RNN_graph: graphs the accuracy vs epoch and validation vs epoch during the training process of RNN.
- RNN_distribution: graphs the sentiment analysis distribution for predicted vs found during the testing process of CNN.
- CNN_results: contains results found using validate.py on CNN.py
- RNN_results: contains results found using validate.py on LSTM.py
- The training process outputs are shown in training_process.txt 

From the training process and results, we can see that: 
- The CNN model runs much more quickly than the LSTM model.
- Both models can achieve a high accuracy for the training dataset after some epochs, but CNN is much more quickly.
- Both models accuracy for the validation dataset are fairly low, meaning that the model is not that good.F1 score is also fairly low.


