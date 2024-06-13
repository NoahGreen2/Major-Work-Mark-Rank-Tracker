import random
from nltk.corpus import words

words = words.words() # List of all English words
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

word = False
set = ''

n = int(input('Enter the number of letters: '))

possible_words = []

for i in words:
    if len(i) == n:
        possible_words.append(i)

while not word:
    letter = random.choice(letters)
    set += letter
    print(letter, end='')
    if len(set) > n-1:
        if set[-(n+1):-1] in possible_words:
            print('\n', set[-(n+1):-1])
            word = True
            break