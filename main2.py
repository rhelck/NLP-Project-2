from os import uname
import numpy as np
import math
import string
import random

from sklearn.model_selection import StratifiedShuffleSplit



#takes input from file

lines = []
testlines = []


testcount = 0
traincount = 0
with open('text3.txt') as f:
    for line in f.readlines():
        #Removes \n
        line = line.strip()
        line = line.translate(str.maketrans('', '', string.punctuation))
        x = random.random()
        if line != "":
            line = "<s> " + line + " </s>"
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

for testline in testlines:
    testsplit_sentence = testline.split()
    for testword in testsplit_sentence:
        #if testword != ("<s>") and testword != ( "</s>"):
        testword = testword.lower()
        testwords.append(testword)
        

#Creates unique list of words in test set
testunique_words = np.unique(testwords)
#print("testuniques: ", testunique_words)

for line in lines:
    #splits each sentence at the space
    split_sentence = line.split()
    for word in split_sentence:
        word = word.lower()
        # if word not in testunique_words:
        #     word = "<UNK>"
        words.append(word)
        

#Creates unigrams for train set
unique_words = np.unique(words)
#print("uniques: ", unique_words)
unigram_counts = dict.fromkeys(unique_words,0)


total_word_count = len(words)
# print("total word count: ", total_word_count)
testtotal_word_count = len(testwords)

for word in words:
    unigram_counts[word] += 1

# print("unigram count: ", unigram_counts)

#Replace all words that only appear once with <UNK>
for word in unigram_counts:
    if unigram_counts[word] <= 15:
        words[words.index(word)] = "<UNK>"

#reruns unique words and unigram counts
#Creates unigrams for train set
unique_words = np.unique(words)
#print("uniques: ", unique_words)
unigram_counts = dict.fromkeys(unique_words,0)

for word in words:
    unigram_counts[word] += 1



#Changes words taht are in test set but not training set with <UNK>
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

# print("bigram counts: ", bigram_count)

#Dictionary of unigram probabilities
p_unigrams = dict.fromkeys(unique_words,0)
for word in unique_words:
    p_unigrams[word] = unigram_counts[word] / total_word_count

# print("unigram probabilities: ", p_unigrams)

#checks to see if unigram probability adds up to one
probabiltiy_check = 0
for probability in p_unigrams:
    probabiltiy_check += p_unigrams[probability]
# print("unigram total probability: ", probabiltiy_check)

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

# print("bigram probabilities: ", p_bigrams)

#checks to see if bigram probability adds up to one
for probability in p_bigrams:
    probabiltiy_check = 0
    for probability2 in p_bigrams[probability]:
        probabiltiy_check += p_bigrams[probability][probability2]
    # print("bigram total probability: ", probabiltiy_check)

add_one_prob_uni = dict()
add_one_prob = dict()

def addOneProb(self, parameter_list):
    #creates unigram add_one
    add_one_prob_uni = dict.fromkeys(unique_words,0)
    for word in unique_words:
        add_one_prob_uni[word] = (unigram_counts[word] + 1) / (total_word_count + len(unique_words))



    # add one
    #add_one_prob = dict()

    #Creates sub dictionary that goes into larger dictionary
    for word in unique_words:
        sub_bigram = dict.fromkeys(unique_words,0)
        add_one_prob[word] = sub_bigram

    #puts subdictionary into the larger dictionary
    for word in unique_words:
        for word2 in unique_words:
            
            add_one_prob[word][word2] =  (bigram_count[word][word2] + 1) / (unigram_counts[word] + len(unique_words))

# print("add_one_prob: ", add_one_prob["I"])

#checks to see if bigram probability adds up to one
for probability in add_one_prob:
    probabiltiy_check = 0
    for probability2 in add_one_prob[probability]:
        probabiltiy_check += add_one_prob[probability][probability2]
    # print("add_one total probability: ", probabiltiy_check)

def generateUnigramSentences(mlebool,k):
    if(mlebool==True):
        for x in range(0,k):
            curr_symbol = "<s>"
            sentence = ""
            sentence_length = 0 # prevent infinite loop
            #while sentence has not ended and the sentence is shorter than the maximum length
            
            while curr_symbol != "</s>" and sentence_length < 20:
                random_value = random.random()
                sumValue = 0
                sentence += " " + curr_symbol
                for i in p_unigrams:
                    sumValue = p_unigrams[i]
                    if((sumValue>random_value)):
                        curr_symbol=i
                        break
                sentence_length += 1
            sentence += " </s>"
            print(sentence)
    if(mlebool==False):
        for x in range(0,k):
            curr_symbol = "<s>"
            sentence = ""
            sentence_length = 0 # prevent infinite loop
            #while sentence has not ended and the sentence is shorter than the maximum length
            
            while curr_symbol != "</s>" and sentence_length < 20:
                random_value = random.random()
                sumValue = 0
                sentence += " " + curr_symbol
                for i in add_one_prob_uni:
                    sumValue = add_one_prob_uni[i]
                    if((sumValue>random_value)):
                        curr_symbol=i
                        break
                sentence_length += 1
            sentence += " </s>"
            print(sentence)    
        

def generateBigramSentences(mlebool,k):
    if(mlebool==True):
        for x in range(0,k):
            curr_symbol = "<s>"
            sentence = ""
            sentence_length = 0 # prevent infinite loop
            #while sentence has not ended and the sentence is shorter than the maximum length
            
            while curr_symbol != "</s>" and sentence_length < 20:
                random_value = random.random()
                sumValue = 0
                sentence += " " + curr_symbol
                for i in p_bigrams[curr_symbol]:
                    sumValue += p_bigrams[curr_symbol][i]
                    if ((sumValue > random_value)):
                        curr_symbol = i
                        break
                # curr_symbol = max(p_bigrams[curr_symbol],key=p_bigrams[curr_symbol].get)
                sentence_length += 1
            sentence += " </s>"
            print(sentence)
    else:
        for x in range(0,k):
            curr_symbol = "<s>"
            sentence = ""
            sentence_length = 0 # prevent infinite loop
            #while sentence has not ended and the sentence is shorter than the maximum length
            while curr_symbol != "</s>" and sentence_length < 20:
                random_value = random.random()
                sumValue = 0
                sentence += " " + curr_symbol
                for i in add_one_prob[curr_symbol]:
                    sumValue += add_one_prob[curr_symbol][i]
                    if ((sumValue > random_value)):
                        curr_symbol = i
                        break
                # curr_symbol = max(p_bigrams[curr_symbol],key=p_bigrams[curr_symbol].get)
                sentence_length += 1
            sentence += " </s>"

            print(sentence)
generateUnigramSentences(mlebool=True,k=5)
generateUnigramSentences(mlebool=False,k=4)
generateBigramSentences(mlebool=True,k=4)
generateBigramSentences(mlebool=False,k=4)

#perplexity calculation for MLE
sumLogMLE = 0
powerAndBase = 10


# perplexity calculation for add-one
i = 0
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
        sumLogPerplexity += math.log(add_one_prob[words[index - 1]][words[index]],powerAndBase)
        #sumLogPerplexity += np.log(add_one_prob[words[index - 1]][words[index]])
        i = i + 1

perplexity = math.pow(powerAndBase, ((-1/testtotal_word_count)*sumLogPerplexity))
        
# print("sumLogPerplexity: " + str(sumLogPerplexity))
# print("n: " + str(testtotal_word_count))
#perplexity = np.exp(((-1/testtotal_word_count)*sumLogPerplexity))
print("Unigram Perplexity: " + str(perplexity_uni))
print("Bigram Perplexity: " + str(perplexity))
# print("i: ",str(i))
#print("percent training: ",str(traincount/(traincount+testcount)))

#Prints the top k most most probable uni grams and their probabilities
def findTopKUnigrams(k):
    for x in range(0,k):
        most_popular = max(p_unigrams, key=p_unigrams.get)
        print(str(most_popular) + ": " + str(unigram_counts[most_popular]) + " : " + str(p_unigrams[most_popular]))
        del p_unigrams[most_popular]
    
#Prints the top ten most most probable bi grams and their probabilities
def findTopKBigrams(k,mlebool):
    #dataTuple = ("",0)
    #top_ten = [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)]
    if(mlebool==True):
        top_ten = [("",0)]*k
        print(top_ten)
        biggest_list = []
        for x in range(0,k):
            biggest_bigram = ("", 0)
            for word in bigram_count:
                for word2 in bigram_count:
                    # print(bigram_count[word][word2])
                    # print(biggest_bigram[1])
                    # print()
                    if bigram_count[word][word2] > biggest_bigram[1]:
                        biggest_bigram = (word + " " + word2, bigram_count[word][word2])

            biggest_bigram = (biggest_bigram[0], bigram_count[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]], p_bigrams[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]])

            #"Removes" the biggest bigram from the data
            bigram_count[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]] = -1

            biggest_list.append(biggest_bigram)
    elif(mlebool==False):
        top_ten = [("",0)]*k
        print(top_ten)
        biggest_list = []
        for x in range(0,k):
            biggest_bigram = ("", 0)
            for word in bigram_count:
                for word2 in bigram_count:
                    # print(bigram_count[word][word2])
                    # print(biggest_bigram[1])
                    # print()
                    if bigram_count[word][word2] > biggest_bigram[1]:
                        biggest_bigram = (word + " " + word2, bigram_count[word][word2])

            biggest_bigram = (biggest_bigram[0], bigram_count[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]], add_one_prob[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]])

            #"Removes" the biggest bigram from the data
            bigram_count[biggest_bigram[0].split()[0]][biggest_bigram[0].split()[1]] = -1

            biggest_list.append(biggest_bigram)

    print(biggest_list)
findTopKBigrams(k=10,mlebool=False)


