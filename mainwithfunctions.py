import numpy as np
import math

#TODO: should probably make a main function and put all other code in functions instead of haveing one long script

#takes input from file
#TODO: should probably make it so user can input a file path/name (in command line when running python file)
lines = []      # lines for training
testlines = []  # lines for testing


def readData(docName, lineName):
    with open(docName) as f:
        for line in f.readlines():
            #Removes \n
            line = line.strip()
            lineName.append(line)


readData('text2.txt',lines)
readData('text.txt',testlines)

# def readLearningData():
#     with open('text2.txt') as f:
#         for line in f.readlines():
#             #Removes \n
#             line = line.strip()
#             lines.append(line)

# def readTestingData():
#     with open('text1.txt') as testf:    #reading data for testing
#         for testline in testf.readlines():
#             #Removes \n
#             testline = testline.strip()
#             testlines.append(testline)

# print("Lines: ", lines)

#creates individual words
#TODO: probably need to add normalization before this to remove punctuation if thats what we want to do
words = []
testwords = []

def create_indiv_words(werds,liens):
    for line in liens:
        #splits each sentence at the space
        split_sentence = line.split()
        for word in split_sentence:
            werds.append(word)

create_indiv_words(words,lines)
create_indiv_words(testwords,testlines)

total_word_count = len(words)

# print("Words: ", words)

#Creates unigrams

unique_words = np.unique(words)
unigram_counts = dict.fromkeys(unique_words,0)

for word in words:
    unigram_counts[word] += 1

# print("unigram count: ", unigram_counts)

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

# print("bigram probabilities: ", p_bigrams["green"])

# sentence generation
def sentence_gen():
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

def add_one_calculations():
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

result_MLE = 0
def perplexity_calc_MLE():
    sumLogMLE = 0
    powerAndBase = 10
    for word in unique_words:
        for word2 in unique_words:
            if(p_bigrams[word][word2]!=0):
                sumLogMLE += math.log(p_bigrams[word][word2],powerAndBase)
    print("sumLogMLE: " + str(sumLogMLE))
    result_MLE = math.pow((-1/total_word_count)*sumLogMLE,powerAndBase)
    print("result: " + str(result_MLE))

#perplexity calculation for add-one
result_Perplexity = 0
def perplexity_calc_add_one():
    sumLogPerplexity = 0
    powerAndBase = 10
    for word in unique_words:
        for word2 in unique_words:
            if(add_one_prob[word][word2]!=0):
                sumLogPerplexity += math.log(add_one_prob[word][word2],powerAndBase)
    print("sumLogPerplexity: " + str(sumLogPerplexity))
    result_Perplexity = math.pow((-1/total_word_count)*sumLogPerplexity,powerAndBase)
    print("result: " + str(result_Perplexity))