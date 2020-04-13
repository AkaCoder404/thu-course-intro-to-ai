# coding=gbk
import numpy as np
import json
import re
import math

py_index = None
hz_index = None
transition = None
pi = None
emissions = None

def readData():
    global py_index, hz_index, transition, pi, emissions
    # Read Data that was previously created during train.py
    pyJson = open('../data/py.json')
    py_index = json.loads(pyJson.read())
    pyJson.close()

    hzJson = open('../data/hz.json')
    hz_index = json.loads(hzJson.read())
    hzJson.close()

    emJson = open('../data/emissions.json')
    emissions = json.loads(emJson.read())
    emJson.close()

    transition = np.load('../data/np_trans.npy')
    pi = np.load('../data/np_pi.npy')


def readInputs(_inputs,_testcases):
    #print("Read Inputs")
    for line in _inputs:
        if re.search(u'[\u4e00-\u9fa6]', line):
            continue
        _testcases.append(line.lower().rstrip('\n').rstrip(' '))

def Veterbi(_testcases, _outputs):
    global py_index, hz_index, transition, pi, emissions
    #print("Viterbi Method")
    obs = []
    for cases in _testcases:
        obs = cases.split(" ")
        #print(obs, end=":") -- print each pinyin sentence

        V = [{}]
        for st in hz_index:
            V[0][st] = {"prob": pi[hz_index[st]] * emissions[st][obs[0]], "prev": None}
        
        # Run Viterbi when t > 0
        for t in range(1, len(obs)): #for each observation
            V.append({})
            short = list(hz_index)
            vshort = list(V[0])[0]
            for st in hz_index: #for each state
                if(V[t-1][vshort]["prob"] == 0 or transition[0][hz_index[st]]==0):
                    max_tr_prob = 0
                else:
                    max_tr_prob = math.log(V[t-1][vshort]["prob"]) + math.log(transition[0][hz_index[st]])
                prev_st_selected = vshort

                if(emissions[st][obs[t]] == 0): #if emission is not possible, don't calculate anything else
                    V[t][st] = {"prob": 0,"prev": prev_st_selected}
                    continue

                for prev_st in short[1:]:
                    if(V[t-1][prev_st]["prob"]==0 or transition[hz_index[prev_st]][hz_index[st]]==0):
                        continue
                    else: 
                        tr_prob = V[t-1][prev_st]["prob"]*transition[hz_index[prev_st]][hz_index[st]]
                    if tr_prob > max_tr_prob:
                        max_tr_prob = tr_prob
                        prev_st_selected = prev_st
                max_prob = max_tr_prob * emissions[st][obs[t]]
                V[t][st] = {"prob": max_prob,"prev": prev_st_selected}        
    
    
        #Get Most probable state and its backtrack
        optimal = []
        max_prob = 0.0 
        for st, data in V[-1].items():
            if data["prob"] > max_prob:
                max_prob = data["prob"]
                best_st = st
        optimal.append(best_st)
        previous = best_st
        
        # Follow the backtrack till the first observation
        for t in range(len(V) - 2, -1, -1):
            optimal.insert(0, V[t + 1][previous]["prev"])
            previous = V[t + 1][previous]["prev"]
        
        optimal = str(optimal).replace('[', '').replace(',','').replace(']','\n').replace('\'','').replace(' ', '')
        print(optimal, end="")
        _outputs.write(optimal)
        
        
def main():
    readData()
    inputs = open('../data/input1.txt', 'r', encoding="GBK")
    outputs = open('../data/output1.txt', 'w', encoding="GBK")
    testcases = []
    readInputs(inputs, testcases)
    inputs.close()
    Veterbi(testcases, outputs)
    outputs.close()    
    
if __name__ == '__main__':
    main()
