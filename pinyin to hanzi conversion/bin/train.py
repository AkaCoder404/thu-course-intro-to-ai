# coding=gbk
import numpy as np
import re
import json

# Read each news txt file and extract 
def readFile(_filename, _inputList):
    print('Reading ' + _filename, end=' ') 
    f = open(_filename, 'r', encoding="GBK")
    for scentence in f:
        _inputList.append(scentence)     
    f.close()

# Access each news txt file
def readNews(_inputList):
    baseFile = '../sina_news_gbk/2016-'
    sources = ['02', '04', '05', '06', '07', '08', '09', '10', '11']
    for src in sources:
        filename = baseFile + src + '.txt'
        readFile(filename, _inputList)

# make a dictionary for pinyin and corresponding hanzi
def pinYinHanZiBiao(_index):
    baseFile = '../拼音汉字表_12710172/拼音汉字表.txt'
    f = open(baseFile, 'r', encoding="GBK")    
    for pinyin in f:
        _index[pinyin.split(' ')[0]] = [a.strip() for a in pinyin.split(' ')[1:]]
    f.close()    
    #save to json file
    hzjson = open('..\data\py.json', 'w')
    json.dump(_index, hzjson)
    hzjson.close()

# make a dictionary for each hanzi and give it an index
def yiErJiHanZiBiao(_index):
    print("make hanzi index")
    baseFile = '../拼音汉字表_12710172/一二级汉字表.txt'
    f = open(baseFile, 'r', encoding="GBK")    
    count = 0
    for line in f:
        for hz in line:
            _index[hz] = count
            count+=1
    f.close()
    #Save to json file
    pyjson = open('..\data\hz.json', 'w')
    json.dump(_index, pyjson)
    pyjson.close()
  
def transition(_inputList, _py_index, _hz_index):
    transition = np.zeros((6763, 6763))
    pi = np.zeros(6763)

    #Strip all sentences so that they only contain Chinese
    sentenceList = []    
    for sentences in _inputList:
        sentenceList.append(re.findall(r'[\u4e00-\u9fa6]+', sentences))
    
    #Head/Starting Matrix
    count = 0
    runtimes = 0
    for sentences in sentenceList:
        for sentence in sentences: 
            if sentence[0] in _hz_index:
                count+=1
                pi[_hz_index[sentence[0]]] += 1
    pi = pi/count
    
    # Transition Matrix
    count = 0
    for sentences in sentenceList:
        for sentence in sentences: 
            for i in range(1, len(sentence)):
                if (sentence[i - 1] in _hz_index) & (sentence[i] in _hz_index):
                    count +=1
                    transition[_hz_index[sentence[i - 1]]][_hz_index[sentence[i]]] += 1
    transition = transition/count
    
    #Emissions Matrix
    emissions = {}
    for hz in _hz_index:
        amt = str(_py_index).count(hz)
        py = {}
        for pyhz in _py_index:
            if hz in _py_index[pyhz]:
                py[pyhz] = 1/amt
            else:
                py[pyhz] = 0
        emissions[hz] = py
    #save to json file 
    emjson = open('..\data\emissions.json', 'w')
    json.dump(emissions, emjson)
    emjson.close()    
    
    #Save numpy arrays
    np.save('../data/np_pi.npy', pi)
    np.save('../data/np_trans.npy', transition)

def main():
    py_index = {} # for pinyin index 拼音汉字表
    hz_index = {} # for hanzi index 一二级子表 
    inputList = [] # for all sentences
    
    readNews(inputList)
    pinYinHanZiBiao(py_index)    
    yiErJiHanZiBiao(hz_index)
    transition(inputList, py_index, hz_index)
  
if __name__ == '__main__':
    main()
