import numpy as np

#TODO: should probably make a main function and put all other code in functions instead of haveing one long script

#takes input form file
#TODO: should probably make it so user can input a file name (in command line when running python file)
lines = []

with open('text.txt') as f:
    for line in f.readlines():
        #Removes \n
        line = line.strip()
        lines.append(line)

# print("Lines: ", lines)

#creates individual words
#TODO: probably need to add normalization before this to remove punctuation if thats what we want to do
words = []
for line in lines:
    #splits each sentence at the space
    split_sentence = line.split()
    for word in split_sentence:
        words.append(word)

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

#Creates sub dictionary that goes into larger dictionary
for word in unique_words:
    sub_bigram = dict.fromkeys(unique_words,0)
    bigram_count[word] = sub_bigram

#puts subdictionary into the larger dictionary
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

#Creates sub dictionary that goes into larger dictionary
for word in unique_words:
    sub_bigram = dict.fromkeys(unique_words,0)
    p_bigrams[word] = sub_bigram

#puts subdictionary into the larger dictionary
for index, word in enumerate(words):
    if index < len(words) and index != 0:
        p_bigrams[words[index - 1]][words[index]] = bigram_count[words[index -1]][words[index]] / unigram_counts[words[index-1]]

# print("bigram probabilities: ", p_bigrams["green"])

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
