'''Get the list of dog breeds to insert into sql database.'''
import os

os.chdir("..")
cwd = os.getcwd()
path = f"{cwd}/dog_images/train"
breeds = os.listdir(path)

dog_list = [(index, breed) for index, breed in enumerate(breeds, 1)]

with open("./db/breeds.txt", "w") as text_file:
    for row in dog_list:
        print(f"{row},", file=text_file)
