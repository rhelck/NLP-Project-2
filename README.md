# NLP-Project-2

## Overview

This is the README file for Project 2 of Dr. Michael Bloodgood's Natural Language Processing (CSC 427-01) class at The College of New Jersey, completed by Robert Helck, Michael Giordano, Geethika Manojkumar, and Poean Lu. This project asked our team to develop bigram and unigram language models implementing the Maximum Liklihood Estimation (MLE) method, as well as the Add-1 smoothing technique, as had been discussed in our class. Additionally, as part of this project our team was asked to perform a variety of experiments using our models and provide written analysis of the results thereof. Additional requirements for the project included (but were not limited to) analyzing the perplexity scores of our models, and finding and normalizing appropriate training and test data.

This README file will provide both an overview of the contents of this package, as well as detailed command line instructions on the proper installation and use of the program.

## Contents

Our package includes the source code of the progam (see main.py), as well as training and text corpora. 
Corpora came from:
1. http://www.nltk.org/nltk_data/ - Australian Broadcasting Commission 2006
File location: \abc\rural.txt
2. http://www.nltk.org/nltk_data/ - Project Gutenberg Selections
File location: \gutenberg\austen-sense.txt

## Requirements

Operating System: Ubuntu 
Compilers: Python 3 
Libraries: Do we need to prompt the user to install numpy etc.?

## Installation

## Use

Type the name of the document used to teach and test the program into the quotation marks in line 38. 
Then, type in python3 main.py into the command line. This runs the python program.
The output will be sentences generated from the most frequently appearing words and phrases,
along with unigram and bigram perplexities and the probability of the most common words that show up in the document.


