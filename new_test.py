import os
import string
import sys, time
alphabet = list(string.ascii_lowercase)

def MultipleChoice(choices, instructions): 
    print(instructions)
    print("This is multiple choice question. Write all letters that you choice")
    for i in range(0, len(choices)-1):
        string_q = alphabet[i] + ") " + str(choices[i])
        print(string_q)
    user_input = input("List your choices: ")
    return_list = []
    for letter in alphabet:
        if letter in user_input:
            return_list.append(choices[alphabet.index(letter)])
    return return_list
write = sys.stdout.write




    