# 拼音输入法作业
pinyin to hanzi conversion project

## Introduction
In the Chinese written language, a given pinyin can have up to 5 different tones
  1. flat
  2. raising
  3. falling-raising
  4. falling
  5. neutral,

each of which can stand for a different Chinese character, or hanzi (汉字). Since the pinyin provided we were provided did not have any tone marks, it becomes much more difficult to discern which character we should convert to. For example, the pinyin "hao" (without tone marks), can be "好", "号", "耗", and so on. Thus, we must use context clues to predict the best possible conversion. Another difficulty that arises is that certain Chinese characters (hanzi) can have different pinyin, this is called 多音字. For example, 行 can be xing, hang, heng, and so on. Thus, we must also create a method to decide which pinyin we should choose when knowing the hanzi.

## Goal
The goal of this project is to take some input, a sentence comprised of pinyin (each of them one space apart), and produce a hanzi conversion of that pinyin. For example, in the given prompt:

|pinyin|hanzi|
|----|----|
|qing hua da xue ji suan ji xi|清华大学计算机系|
|wo shang xue qu le|我上学去了|
|jin tian hui jia bi jiao wan|今天回家比较晚|
|liang hui zai bei jing zhao kai|两会在北京召开|

## Implementation
This algorithm implements a word-based binary model conversion from pinyin to Chinese Characters.
After researching multiple methods, the one I found most suited to achieve this goal was to utilize a Hidden Markov Model and the Viterbi algorithm. After comparing to different methods, I found that this method fit the project discription perfectly, and that it would hopefully allow us to achieve a pretty high accuracy. 

A Hidden Markov Model, or HMM, is a statistical model that allows us to predict a "hidden process", by observing another one who's behavior depends on the "hidden process". In this project, the hidden states are the hanzi, for example, 清，华，大，学，and so forth. The observable states are the pinyin, for example, qing, hua, da, xue. So, we would see a sequence of observables (piynin), but we would not know the hidden states (characters given by the 一二级汉字表), from which the observations were  generated from. However, we do know the probabilities that a hidden state generates an observation (known as emission), the possibility that a given character comes after another (known as transition), and the possibility that a given character occurs (known as start or head). The data we use to find these probabilities is generated from articles taken from sina news, located in "sina_news_gbk" (file not included in git because file is too large). Then, the HMM can be seen as a graph, and the Viterbi algorithm would help find the optimal path through the graph, or in other terms, the best possible covnersion from pinyin to hanzi.

## Code
I split up the implementation into 3 different parts (located in bin): train.py, viterbi.py, and core.py:

  - train.py: since working with such large data sets (those located in sina_news_gbk), I first “trained” my data so that I wouldn’t have to every time we tested for new inputs. This part of the code compiles the data into data structures. I would store and generate the necessary data in python dictionaries and numpy arrays. I would then store the python dictionary in a json file, and use numpy’s .save function to save the data into a .npy file.
  - viterbi.py: this section iterates through each of the inputs (pinyin sentences) and performs the Viterbi algorithm on each sentence. 
  - score.py: in order to check the accuracy of the algorithm, I compared the algorithm’s output to the correct output.
  
## Experimental Results
The standard inputs and accuracy are as follows.

||pinyin|output|expected answer|accuracy|
|-|----|----|---------|--------|
|1|qing hua da xue ji suan ji xi|清华大学计算机系|清华大学计算机|8/8|
|2|wo shang xue qu le|我上学去了|我上学去了|5/5|
|3|jin tian hui jia bi jiao wan|今天回家比较完|今天回家比较晚|6/7|
|4|liang hui zai bei jing zhao kai|两会在北京召开|两会在北京召开|7/7|

Thus, this gives us a accuracy of about 96%.

I tested another group of inputs that was given by a student in the class group wechat. It contained about 800 test cases. The results can be found in the src (score 2). It produced an accuracy of about 73%. Although at first, this seems fairly inaccurate, with only a 3/4 probability of giving the correct pinyin to hanzi conversion, but after analyzing the results, there is a an obvious trend of the type of inaccuraces. A considerable amout of these inaccuracies is due to the fact that the data set is limited to news sources. This will be explained further in the conclusion.

## Conclusion
Conclusion: 
The viterbi algorithm I used could definitely be improved for efficiency. One improvement would be to fully utilize numpy arrays, instead of using a combination of numpy arrays and json files. Fully using numpy arrays would allow my algorithm to calculate the probabilities and selecting the optimal path (optimal conversion) more quickly. For example, I could utilize np’s .log function. Instead of multiplying values, which takes a longer time, I could utilize .log function to add two values. 
Regarding the accuracy of the program, I believe, is quite good for the data it had to work with. Since the data we worked with was exclusively from news articles, this will be good for consistency in the results, and those more accurate. However, the most optimal conversion (of the sentences) will be taken as if it was in a news article, even if it wasn’t intended to. For example, idioms and slag phrases, which usually don’t appear in formal news articles, will have poor pinyin to hanzi translations. Inorder to improve this accuracy would be to give it more data sets to work with, perhaps include texts written in the cultural or casual context. The second test case’s accuracy dropped significantly since a significant portion of the errors occurred in idiom translations, or phrases that might not appear as often in news articles.
Another way to improve this program is if we were given the pinyin for the actual characters. Using this, we could improve the emissions matrix, or the probability that 行 is xing rather than hang by calculating the amount of time xing appears over hang for 行. But, given the data set that we are working with, this isn’t as necessary and may not improve accuracy by that much.



