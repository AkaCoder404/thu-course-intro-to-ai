#coding=gbk
from prettytable import PrettyTable as pt 
import re

def main():
    input1 = '../data/input1.txt'  #Original Test Case
    input2 = '../data/input2.txt' #Extra Test Case
    output1 = '../data/output1.txt' #Original Test Case
    output2 = '../data/output2.txt' #Extra Test Case
    correctfile1 = '../data/correct_output_1.txt' # correct output for test case 1
    correctfile2 = '../data/correct_output_2.txt' # correct output for test case 2

    correct_output = open(correctfile1, 'r', encoding="GBK")
    check_output = open(output1, 'r', encoding="GBK")
    py_input = open(input1, 'r', encoding="GBK")

    score = list()
    total_checks = 0
    total_correct = 0

    for correct, check, py in zip(correct_output, check_output, py_input):
        sentence = list()
        correct = correct.replace(" ", '').rstrip("\n")
        check = check.replace(" ", '').rstrip("\n")
        py = py.rstrip("\n")
        sentence.append(str(py))
        sentence.append(str(correct))
        sentence.append(str(check))
        total_char_py = len(correct)
        total_checks += total_char_py
        num_correct = 0
        for a, b in zip(correct, check):
            # print(a + " " + b)
            if a == b:
                num_correct+=1
                total_correct+=1
        sentence.append(str(num_correct)+"/"+ str(total_score))
        # print(str(num_correct)+"/"+ str(total_score))
        score.append(sentence)

    x = pt(["Pinyin", "Correct", "Mine", "Score"])
    x.align["Correct"] = "l"
    x.align["Mine"] = "l"
    x.align["Score"] = "l"
    x.align["Pinyin"] = "l"
    x.padding_width = 1
    for a in score:
        x.add_row([a[0], a[1], a[2], a[3]])

    with open('../src/score.txt', 'w', encoding = "GBK") as score:
        score.write("Reading from " + input2 + "and compare to " + correctfile2 + "\n")
        score.write(str(x))
        score.write("\nTotal Percentage Correct " + str(total_correct/total_checks))

if __name__ == '__main__':
    main()
