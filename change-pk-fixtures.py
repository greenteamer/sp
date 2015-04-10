#!/usr/bin/env python
with open('fixt.json', 'r') as f:
    read_data = f.read()
    data = read_data.split("\n")
    i = 0
    for line in data:
        if '"pk": ' in line:
            if i == 0:
                curent_number = int(line[10:12]) - 1
            number = int(line[10:12]) - curent_number
            text = line[0:10] + str(number) + line[12:]
            print text
            i += 1
        else:
            print line
f.close()