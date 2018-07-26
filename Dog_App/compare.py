'''Compare with udacity dataset'''

import os
import re

files = os.listdir()
breeds = list(map(lambda x: re.sub('^\d*\.', '', x), files))

def create_breed_list(path, name, breeds):
    with open(f"{path}/{name}.txt", 'w') as outfile:
        for item in breeds:
            outfile.write(str(item) + '\n')

def read_file(path, file):
    # Read in file and convert to sets
    with open(f"{path}/{file}", 'r') as infile:
        lines = set([re.sub("s$", '', line.strip().lower()) for line in infile])

    return lines

def compare_lists(udacity, mine):
    intersection = udacity & mine
    difference = udacity - mine
