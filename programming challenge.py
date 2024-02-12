f = open('myfile.txt', 'r')
filestring = f.read()
print('File contents: ')
print(filestring)
vowels = ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U']
consonants = ['b', 'B', 'c', 'C', 'd', 'D', 'f', 'F', 'g', 'G', 'h', 'H',
                'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'p', 'P',
                'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'v', 'V', 'w', 'W',
                'x', 'X', 'y', 'Y', 'z', 'Z']
vowel_count = 0
consonant_count = 0
char_count = 0
for i in filestring:
    if i in vowels:
        vowel_count += 1
    elif i in consonants:
        consonant_count += 1
for char in filestring:
    char_count += 1
print()
print('Characters: ' + str(char_count))
print('Vowels: ' + str(vowel_count))
print('Consonants: ' + str(consonant_count))

