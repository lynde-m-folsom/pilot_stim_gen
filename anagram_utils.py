# functions for making anagrams from wordnet for a given word length

# imports
from nltk.corpus import wordnet as wn
from wordfreq import zipf_frequency
import random
import itertools


# function: make a dictionary of words from wordnet for a given word length
def mk_dict_from_wordnet_for_length(word_length):
    # words have synset of length 3 after splitting by "."
    synset_length = 3
    # lemmas are keys and definitions are values
    selected_words = {}
    for synset in wn.all_synsets():
        if len(synset.name().split(".")) == synset_length:
            if len(synset.name().split(".")[0]) == word_length:
                word = synset.name().split(".")[0]
                if word.isalpha():
                    selected_words[word] = synset.definition()     
    return selected_words

# function to remove a list words (like curse words) # modified to remove from list or dict
def remove_from_dict(word_dict, word_list):
    if isinstance(word_dict, dict):
        for word in word_list:
            if word in word_dict:
                del word_dict[word]
    elif isinstance(word_dict, list):
        word_dict = [word for word in word_dict if word not in word_list]
    return word_dict

# function: get word frequencies for a given word as a dictionary
def get_word_frequencies(word_dict, minfrequency=1):
    word_frequencies = {}
    for wordlength in word_dict.keys():
        word_frequencies[wordlength] = {}
        for word in word_dict[wordlength]:
            freq = zipf_frequency(word, "en")
            if freq >= minfrequency:
                word_frequencies[wordlength][word] = freq
    return word_frequencies

# function: sort words by frequency
def sort_words_by_frequency(word_frequencies):
    sorted_word_frequencies = {}
    for wordlength, wordfreq_by_length in word_frequencies.items():
        sorted_word_frequencies[wordlength] = sorted(
            wordfreq_by_length,
            key=wordfreq_by_length.get,
            reverse=True)
    return sorted_word_frequencies

#function to take sorted_wordlist and return it in a format for using get_top_n_words
def reformat_sorted_wordlist(sorted_wordlist):
    column_lists = [list(value) for value in sorted_wordlist.values()]
    sorted_wordlist = list(zip(*column_lists))
    return sorted_wordlist

# function: get the top n words from a sorted distribution, need to add a propesition of word length
def get_top_n_words(sorted_fdist, n):
    # Get the top n sublists
    top_n_sublists = sorted_fdist[:n]
    # Flatten the list of lists
    full_list = [word for sublist in top_n_sublists for word in sublist]
    return full_list


#function to shuffle the letters and append to the list
def shuffle_letters(word):
    shuffled = list(word)
    random.shuffle(shuffled)
    shuffled_word = "".join(shuffled)
    return shuffled_word

#function that takes a list uses the shuffle letters function and returns a list of shuffled words
def shuffle_list(cat_full_list):
    shuffled_list = []
    for word in cat_full_list:
        shuffled_list.append(shuffle_letters(word))
    return shuffled_list

#function to review the cat list and find doubles in the shuffled column and to shuffle again, then return that word to the list
def check_for_doubles(cat_full_list):
    for index, row in cat_full_list.iterrows():
        if row['root'] == row['shuffled']:
            cat_full_list.at[index, 'shuffled'] = shuffle_letters(row['root'])
    return cat_full_list

#function to check that the shuffled word is not the same as the root word and reshuffle if it is
def check_for_same(cat_full_list):
    for index, row in cat_full_list.iterrows():
        if row['root'] == row['shuffled']:
            cat_full_list.at[index, 'shuffled'] = shuffle_letters(row['root'])
    return cat_full_list

#function to check if the word is in the dictionary (needed for function below)
def check_word(word, word_list):
    return word in word_list
    
#function for finding the possible words made out of the string of letters in shuffled, we are calling these the valid words
def find_valid_words(input_string, word_dict):
     valid_words = []
     permutations = ["".join(i) for i in itertools.permutations(input_string)]
     input_length = len(input_string)
     for candidate in permutations:
         result = check_word(candidate, word_dict[input_length])
         if result:
             valid_words.append(candidate)
     return valid_words 