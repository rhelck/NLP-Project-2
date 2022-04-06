# NLP-Project-2

## Overview

This is the README file for Project 2 of Dr. Michael Bloodgood's Natural Language Processing (CSC 427-01) class at The College of New Jersey, completed by Robert Helck, Michael Giordano, Geethika Manojkumar, and Poean Lu. This project asked our team to develop bigram and unigram language models implementing the Maximum Likelihood Estimation (MLE) method, as well as the Add-1 smoothing technique, as had been discussed in our class. Additionally, as part of this project, our team was asked to perform a variety of experiments using our models and provide a written analysis of the results thereof. Additional requirements for the project included (but were not limited to) analyzing the perplexity scores of our models, and finding and normalizing appropriate training and test data.

This README file will provide both an overview of the contents of this package, as well as detailed command-line instructions on the proper installation and use of the program.

## Contents

Our package includes the source code of the program (see main.py), as well as training and text corpora. 
Corpora came from:
1. http://www.nltk.org/nltk_data/ - Australian Broadcasting Commission 2006
File taken from: \abc\rural.txt
2. http://www.nltk.org/nltk_data/ - Project Gutenberg Selections
File taken from: \gutenberg\austen-sense.txt

Source files in folder:
- austin.txt - text file of 'Sense and Sensibility' by Jane Austin
- australia_rural.txt - text file containing news reports from the Australian Broadcast Company
- D2.txt - write up of statistics required for D2 deliverable
- D3.txt - write up of feedback required for D3 deliverable
- main.py - main python code that can be executed by the user to run the program
- README.md - this file that explains the contents to the user

## Requirements

Operating System: Ubuntu 
Language: Python 3.7.5 

## Installation

In the ELSA command line run:
$ module add python/3.7.5

## Use

This program is designed to be used from the terminal. Once the user has entered the directory where they have unzipped the tar.gz 
file, the user will enter "python3 main.py file.txt", where file.txt is the corpus that the user would like to use. For convenience, we
have included two corpora in our package, however, the user is free to enter the full path to another .txt file that they would like to 
use instead. If the program cannot locate the file, the user will be prompted for a new file until a usable file path is entered.
After this, the user is prompted to enter either "MLE" or "Add-1". This allows the user to choose whether to use Maximum Likelihood or,
Add-1 smoothing (NOTE: only Add-1 is available, there is no support for Add-k smoothing where k!=1). If the user does 
not enter "MLE" or "Add-1", the user will continue to be prompted to do so.

This program will report the perplexity scores for the unigram and bigram models (measured on the held-out data from the corpus specified from the 
user) on the command line, as well as the 5 most common sentences generated from the bigram and unigram models, and the 10 most common unigram and 
bigrams for the respective models.


## Notes

Normalization:
- All punctuation is removed and replaced with spaces.
- All text is changed to lower case
- Each "sentence" starts with "<s>" and ends with "</s>".

Outputs:
- Sentences stop when the "</s>" or 20 characters are in the sentence
- For the chosen task, output includes:
    1. Unigram Perplexity
    2. Bigram Perplexity
    3. Unigram MLE sentences
    4. Bigram MLE sentences
    5. Top 10 MLE Unigrams
    6. Top 10 MLE Bigrams
-For sentence output, 5 sentences are given according to pdf instructions
-As the purpose of this assignment is a learning experience, "<UNK>" was left in the generated sentence. In an actual appliation of this software, "<UNK>" would potentiall want to be removed
-Addiionally "<s>" and "</s>" were used in the sentences. In an actual implementation, these may be removed.
-For Top 10 outputs, format is "[uni/bi]gram : # of occurrences of [uni/bi]gram : [MLE/Add-1] probability"
