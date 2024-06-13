from PyDictionary import PyDictionary
from nltk.corpus import words
import random

words = words.words()

dictionary = []

for i in words:
    dictionary.append(PyDictionary(i))

word = random.choice(words)
definition = dictionary.meaning(word)
print(definition)
guess = str(input("What is this word?: ")).lower()
if guess == word:
    print("Correct!")
else:
    print("Incorrect!")
    print(f"The word was {word}")
