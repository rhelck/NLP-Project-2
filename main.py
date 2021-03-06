from os import uname
import numpy as np
import math
import string
import random
import sys
import os.path

from sklearn.model_selection import StratifiedShuffleSplit

#takes input from file
lines = []
testlines = []
filename = sys.argv[1]
method = ""
if(len(sys.argv)<2):
    print("Incorrect number of arguments given, please type:\n python3 main.py path_to_text_file method \n where method is either 'MLE' or 'Add-1'")
while(os.path.exists(filename)==False):
    print("The file you entered was not found, please enter the full path of your desired .txt file to use as your corpus.")
    filename = input()
while((method!="MLE" and method!="Add-1")):
    print("Would you like to use MLE, or Add-1 smoothing? Enter MLE or Add-1.") 
    method = input()

testcount = 0
traincount = 0
with open(filename) as f:
    for line in f.readlines():
        line = line.strip()
        line = line.translate(str.maketrans('', '', string.punctuation))
        x = random.random()
        if line != "":
            line = "<s> " + line + " </s>"
            #Splits the given data into a training set and a held out test set 
            if(x<=.75):
                lines.append(line)
                testcount = testcount + 1
            else:
                testlines.append(line)
                traincount = traincount + 1
    f.close()

#creates individual words
words = []
testwords = []

def makeWords(linesparam,wordsparam):
    for line in linesparam:
        split_sentence = line.split()
        for word in split_sentence:
            word = word.lower()
            wordsparam.append(word)

makeWords(lines,words)
makeWords(testlines,testwords)

#Creates unique list of words in test set
testunique_words = np.unique(testwords)

#Creates unigrams for train set
unique_words = np.unique(words)
unigram_counts = dict.fromkeys(unique_words,0)

total_word_count = len(words)
testtotal_word_count = len(testwords)

for word in words:
    unigram_counts[word] += 1

#Replace all words that only appear once with <UNK>
for word in unigram_counts:
    if unigram_counts[word] <= 1:
        words[words.index(word)] = "<UNK>"

#reruns unique words and unigram counts
#Creates unigrams for train set
unique_words = np.unique(words)
unigram_counts = dict.fromkeys(unique_words,0)

for word in words:
    unigram_counts[word] += 1

#Changes words that are in test set but not training set with <UNK>
for word in testwords:
    if word not in unique_words:
        testwords[testwords.index(word)] = "<UNK>"

#creates bigrams
bigram_count = dict()

#Creates nested dictionary
total_bigrams = 0
for word in unique_words:
    sub_bigram = dict.fromkeys(unique_words,0)
    bigram_count[word] = sub_bigram
    total_bigrams += 1
total_bigrams *= len(unique_words)

#finds counts of bigrams
for index, word in enumerate(words):
    #This condition guarantees that we do not overcount the bigram of {<s>,</s>}, or whatever the start and end characters are in the document.
    if index < len(words) and index != 0:
        bigram_count[words[index - 1]][words[index]] += 1

#Dictionary of unigram probabilities
p_unigrams = dict.fromkeys(unique_words,0)  
for word in unique_words:
    p_unigrams[word] = unigram_counts[word] / total_word_count

#Dictionary of bigram probabilities
p_bigrams = dict()

#Creates nested dictionary
for word in unique_words:
    sub_bigram = dict.fromkeys(unique_words,0)
    p_bigrams[word] = sub_bigram

#updates dictionary with MLE probailities
for index, word in enumerate(words):
    if index < len(words) and index != 0:
        p_bigrams[words[index - 1]][words[index]] = bigram_count[words[index - 1]][words[index]] / unigram_counts[words[index - 1]]

#creates unigram add_one
add_one_prob_uni = dict.fromkeys(unique_words,0)
for word in unique_words:
    add_one_prob_uni[word] = (unigram_counts[word] + 1) / (total_word_count + len(unique_words))

# add one 
add_one_prob = dict()   
# stores all add_one probabilities

#Creates sub dictionary that goes into larger dictionary
for word in unique_words:
    sub_bigram = dict.fromkeys(unique_words,0)
    add_one_prob[word] = sub_bigram

#puts subdictionary into the larger dictionary
for word in unique_words:
    for word2 in unique_words:
        add_one_prob[word][word2] =  (bigram_count[word][word2] + 1) / (unigram_counts[word] + len(unique_words))

#perplexity calculation for MLE
sumLogMLE = 0
powerAndBase = 10

# perplexity calculation for add-one
sumLogPerplexity_uni = 0
sumLogPerplexity = 0
powerAndBase = 10

#add_one unigram perplexity
for word in testwords:
    sumLogPerplexity_uni += math.log(add_one_prob_uni[word],powerAndBase)

perplexity_uni = math.pow(powerAndBase, ((-1/testtotal_word_count)*sumLogPerplexity_uni))

#add_one bigram perplexity
for index, word in enumerate(testwords):
    if index < len(testwords) and index != 0:
        sumLogPerplexity += math.log(add_one_prob[words[index-1]][words[index]],powerAndBase)

perplexity = math.pow(powerAndBase, ((-1/testtotal_word_count)*sumLogPerplexity))
print()
print("Unigram Perplexity: " + str(perplexity_uni))
print("Bigram Perplexity: " + str(perplexity))
print()

def generateUnigramSentences(mlebool,k):
    #ARGUMENTS: mlebool: decides whether to use MLE or Add-1 model
            #k: decides the number of sentences to produce
    if(mlebool==True):
        dictionary = p_unigrams
    else:
        dictionary = add_one_prob_uni
    for x in range(0,k):
        #Generate k sentences.
        curr_symbol = "<s>"
        sentence = ""
        sentence_length = 0
        while curr_symbol != "</s>" and sentence_length < 20:
            #while sentence has not ended and the sentence is shorter than the maximum length
            random_value = random.random()
            sumValue = 0
            sentence += " " + curr_symbol
            for i in dictionary:
                sumValue += dictionary[i]
                if((sumValue>random_value)):
                    curr_symbol=i
                    break
            sentence_length += 1
        sentence += " </s>"
        print(sentence)
    #RETURN: this function is a void function, as such it returns nothing; it's purpose is to print generated sentences with the unigram langauge model.

def generateBigramSentences(mlebool,k,length):
    #ARGUMENTS: mlebool: decides whether to use MLE or Add-1 model
            #k: decides the number of sentences to produce
            #(int) length: decides the maximum length of sentences
    if(mlebool==True):
        dictionary = p_bigrams
    else:
        dictionary = add_one_prob

    for x in range(0,k):
        curr_symbol = "<s>"
        sentence = ""
        sentence_length = 0             
        while curr_symbol != "</s>" and sentence_length < length:
            #while sentence has not ended and the sentence is shorter than the maximum length
            random_value = random.random()
            sumValue = 0
            sentence += " " + curr_symbol
            for i in dictionary[curr_symbol]:
                sumValue += dictionary[curr_symbol][i]
                if ((sumValue > random_value)):
                    curr_symbol = i
                    break
            sentence_length += 1
        sentence += " </s>"
        print(sentence)
    #RETURN: this function is a void function, as such it returns nothing; it's purpose is to print generated sentences with the bigram langauge model.

#Only runs the code depending on what the user wants
if(method=='MLE'):
    print("Unigram MLE sentences")
    generateUnigramSentences(mlebool=True,k=5)
    print()
    print("Bigram MLE sentences")
    generateBigramSentences(mlebool=True,k=5,length=20)
    print()
elif(method=='Add-1'):
    print("Bigram Add-1 sentences")
    generateBigramSentences(mlebool=False,k=5,length=20)
    print()
    print("Unigram Add-1 sentences")
    generateUnigramSentences(mlebool=False,k=5)
    print()

def findTopKBigrams(k,mlebool):
    #ARGUMENTS: k:  the top k number of bigrams to find (k=10 as per the assignment's instructions).
    #           mlebool:   this decides whether we use MLE or Add-1 smoothing.

    if(mlebool==True):
        dictionary = p_bigrams
    else:
        dictionary = add_one_prob
    top_ten = [("",0)]*k
    biggest_list = []
    for x in range(0,k):
        biggest_bigram = ("", 0)
        for word in bigram_count:
            for word2 in bigram_count:
                if bigram_count[word][word2] > biggest_bigram[1]:
                    biggest_bigram = (word + " " + word2, bigram_count[word][word2])

        biggest_bigram = (biggest_bigram[0], bigram_count[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]], dictionary[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]])
        bigram_count[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]] = -1
        biggest_list.append(biggest_bigram)

    for bigram in biggest_list:
        print(str(bigram[0].split()[0]) + " " + str(bigram[0].split()[1]) + " : " + str(bigram[1]) + " : " + str(bigram[2]))
    #RETURN:    this function does not return anything, instead it prints the top k most likely bigrams onto the command line for the user.

def findTopKUnigrams(k,mlebool):
    #ARGUMENTS: k:  the number of unigrams to report, i.e. the k most likely unigrams.
                #mlebool: wether to use MLE or, if false, Add-1 smoothing.
    if(mlebool==True):
        for x in range(0,k):
            most_popular = max(p_unigrams, key=p_unigrams.get)
            print(str(most_popular) + ": " + str(unigram_counts[most_popular]) + " : " + str(p_unigrams[most_popular]))
            del p_unigrams[most_popular]
    else:
        for y in range(0,k):
            most_popular = max(add_one_prob_uni, key=add_one_prob_uni.get)
            print(str(most_popular) + " : " + str(unigram_counts[most_popular]) + " : " + str(add_one_prob_uni[most_popular]))
            del add_one_prob_uni[most_popular]
    #RETURN:    this function does not return anything, instead it prints the top k most likely bigrams onto the command line for the user.
    #NOTE: this function deletes k most common unigrams from whichever dictionary (that is, MLE or Add-1) is chosen by mlebool.

#Only runs the code depending on what the user wants
if(method=="Add-1"):
    print("Top 10 add-1 Unigrams")
    print("unigram : # of occurances : add-1 probability")
    findTopKUnigrams(k=10,mlebool=False)
    print()
    print("Top 10 add-1 Bigrams")
    print("bigram : # of occurances : add-1 probability")
    findTopKBigrams(k=10,mlebool=False)
    print()
elif(method=="MLE"):
    print("Top 10 MLE Unigrams")
    print("unigram : # of occurances : MLE probability")
    findTopKUnigrams(k=10,mlebool=True)
    print()
    print("Top 10 MLE Bigrams")
    print("bigram : # of occurances : MLE probability")
    findTopKBigrams(k=10,mlebool=True)
    print()