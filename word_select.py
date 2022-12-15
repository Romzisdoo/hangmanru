import random

WORDLIST = "dictionary/1655.txt"

def get_random_word(): 
    num_words_processed = 0
    curr_word = None
    with open(WORDLIST, 'r') as f:
        for word in f:
            word = word.strip().lower()
            num_words_processed += 1
            if random.randint(1, num_words_processed) == 1:
                curr_word = word
    return curr_word