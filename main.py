from os import uname
import numpy as np
import math
import string

from sklearn.model_selection import StratifiedShuffleSplit

#TODO: should probably make a main function and put all other code in functions instead of haveing one long script

#takes input from file
#TODO: should probably make it so user can input a file path/name (in command line when running python file)
lines = []
testlines = []

with open('text3.txt') as f:
    for line in f.readlines():
        #Removes \n
        line = line.strip()
        line = line.translate(str.maketrans('', '', string.punctuation))
        if line != "":
            line = "<s> " + line + " </s>"
            lines.append(line)
    f.close()

with open('text2.txt') as testf:    #reading data for testing
    for testline in testf.readlines():
        #Removes \n
        testline = testline.strip()
        testline = testline.translate(str.maketrans('', '', string.punctuation))
        if testline != "":
            testline =  "<s> " + testline + " </s>"
            testlines.append(testline)
    f.close()

# print(lines)

# print("Lines: ", lines)

#creates individual words
#TODO: probably need to add normalization before this to remove punctuation if thats what we want to do
words = []
testwords = []

for testline in testlines:
    testsplit_sentence = testline.split()
    for testword in testsplit_sentence:
        #if testword != ("<s>") and testword != ( "</s>"):
        testword = testword.lower()
        testwords.append(testword)
        # print(testword)

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
        # print(word)

#Creates unigrams for train set
unique_words = np.unique(words)
#print("uniques: ", unique_words)
unigram_counts = dict.fromkeys(unique_words,0)

#print(words)
#print(testwords)

total_word_count = len(words)
testtotal_word_count = len(testwords)

for word in words:
    unigram_counts[word] += 1

# print("unigram count: ", unigram_counts)

#Replace all words that only appear once with <UNK>
for word in unigram_counts:
    if unigram_counts[word] == 1:
        words[words.index(word)] = "<UNK>"

#reruns unique words and unigram counts
#Creates unigrams for train set
unique_words = np.unique(words)
#print("uniques: ", unique_words)
unigram_counts = dict.fromkeys(unique_words,0)

total_word_count = len(words)
testtotal_word_count = len(testwords)

for word in words:
    unigram_counts[word] += 1

# print("unigram counts with UNK: ", unigram_counts)

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

#updates disctionary with MLE probailities
for index, word in enumerate(words):
    if index < len(words) and index != 0:
        p_bigrams[words[index - 1]][words[index]] = bigram_count[words[index - 1]][words[index]] / unigram_counts[words[index - 1]]

print("bigram probabilities: ", p_bigrams)

#checks to see if bigram probability adds up to one
probabiltiy_check = 0
for probability in p_bigrams:
    for probability2 in p_bigrams[probability]:
        probabiltiy_check += p_bigrams[probability][probability2]
print("bigram total probability: ", probabiltiy_check)

# sentence generation
curr_symbol = "<s>"
sentence = ""
sentence_length = 0 # prevent infinite loop
while curr_symbol != "</s>" and sentence_length < 20:
    sentence += " " + curr_symbol
    curr_symbol = max(p_bigrams[curr_symbol],key=p_bigrams[curr_symbol].get)
    sentence_length += 1
sentence += " </s>"
print(sentence)

# add one
add_one_prob = dict()

#Creates sub dictionary that goes into larger dictionary
for word in unique_words:
    sub_bigram = dict.fromkeys(unique_words,0)
    add_one_prob[word] = sub_bigram

#puts subdictionary into the larger dictionary
# for index, word in enumerate(words):
#     if index < len(words) and index != 0:
#         add_one_prob[words[index - 1]][words[index]] = (bigram_count[words[index -1]][words[index]] + 1) / (unigram_counts[words[index-1]] + len(unique_words))
        # print((bigram_count[words[index -1]][words[index]] + 1) / (unigram_counts[words[index-1]] + len(unique_words)))

#puts subdictionary into the larger dictionary
for word in unique_words:
    for word2 in unique_words:
        # print("word: "+word+" word2: "+word2)
        add_one_prob[word][word2] =  (bigram_count[word][word2] + 1) / (unigram_counts[word] + len(unique_words))

# print("add_one_prob: ", add_one_prob["I"])

#perplexity calculation for MLE

sumLogMLE = 0
powerAndBase = 10
# print(p_bigrams)
# print(unique_words)
# print(testunique_words)
for word in testunique_words:
    for word2 in testunique_words:
        # print(p_bigrams[word][word2])
        if not ((word in p_bigrams.keys()) and (word2 in p_bigrams[word].keys())): #and (p_bigrams[word].has_key(word2)):
            # print(p_bigrams[word]["<UNK>"])
            sumLogMLE += math.log(p_unigrams["<UNK>"],powerAndBase)
            # sumLogMLE += math.log(p_bigrams[word]["<UNK>"],powerAndBase)
        elif(p_bigrams[word][word2] != 0):
            # print("elif")
            sumLogMLE += math.log(p_bigrams[word][word2],powerAndBase)
print("sumLogMLE: " + str(sumLogMLE))
perplexity = math.pow((-1/total_word_count)*sumLogMLE,powerAndBase)
print("PP(W): " + str(perplexity))

# perplexity calculation for add-one
# sumLogPerplexity = 0
# powerAndBase = 10
# for word in unique_words:
#     for word2 in unique_words:
#         if(add_one_prob[word][word2]!=0):
#             sumLogPerplexity += math.log(add_one_prob[word][word2],powerAndBase)
# print("sumLogPerplexity: " + str(sumLogPerplexity))
# perplexity = math.pow((-1/total_word_count)*sumLogPerplexity,powerAndBase)
# print("PP(W): " + str(perplexity))