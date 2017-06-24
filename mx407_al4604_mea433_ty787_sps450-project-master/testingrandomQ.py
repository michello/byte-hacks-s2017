from random import randint
from tkinter import messagebox
import tkinter as tk

def generateFact():
    ## pop up for killing/add this at the end:
    facts = ['You can save a value to a variable using an equal sign! \n For example, x = 10',
                'Variable names are ',
                'You can print words using the print function. \n For example, by typing: \n print("Hello world!");\n You are typing, "Hello world!"',
                'A string is a collection of characters surrounded by quotes \n For example, "This is a string" is a string',
                'You can save a string to a variable using the equal sign. \n For example, string_var = "A string"',
                '']
    return(messagebox.showinfo(facts[randint(0, len(facts) - 1)], 'hello'))
