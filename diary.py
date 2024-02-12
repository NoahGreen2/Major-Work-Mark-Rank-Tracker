
while True:
    f = open('diary.txt', 'r+')
    mode = input('Would you like to read or write? ')
    if mode == 'read' or mode == 'Read':
        entry = int(input('What entry would you like to read? '))
        entry = entry - 1
        filestring = f.read()
        filelist = filestring.split('\n')
        print(filelist[entry])
    elif mode == 'write' or mode == 'Write':
        entry = input('What would you like to write? ')
        f.write(entry + '\n')

    