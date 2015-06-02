#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')

    return parser


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()
    try:
        file = namespace.file
        with open(file, 'r') as f:
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
    except:
        print ("введи имя файла через -f или --file")
