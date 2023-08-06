import random
from time import sleep as wt
import pyfiglet
from pynput.keyboard import Controller



def write_like_gpt(text,waite=0.01):
    for echar in text:
        print(echar,end="",flush=True)
        wt(waite)
    print()

def write_in_underscore(text,waite=0.01):
    for echar in text:
        print(echar,end="_",flush=True)
        wt(waite)
    print()

def write_in_mono(text,waite=0.01):
    for echar in text:
        print(echar,end=" ",flush=True)
        wt(waite)
    print()

def write_in_ascii(text:str)->str:
    # Use pyfiglet to convert the text to ASCII art
    ascii_art = pyfiglet.figlet_format(text)
    # typing the ASCII art to the console
    write_like_gpt(ascii_art)


def write_in_3d_underscore(text,waite=0.01):
    for echar in text:
        print(echar,end="__",flush=True)
        wt(waite)
    print()


def console_overwrite_typing(text):
    for i in range(len(text)):
        print(text[:i+1], end='\r', flush=True)
        wt(0.1) # adjust the delay as needed
    print()

# example usage
# overwrite_typing("Hello, world!")
# wt(1) # add a pause before modifying the text
# overwrite_typing("My Name is Abdullah")
# wt(5) # add a pause before modifying the text

def real_type(text):
    # wt(5)
    key = Controller()
    for tychar in text:
        key.type(tychar)
        wt(0.1)

# real_time_typeing("may people here a course very again they present group hold problem well may also most want such when but point well need face if all house down off hold program think own person he between eye without present face back you find through nation")

def write_in_flash_line(text):
    for i in range(len(text)):
        if i % 2 == 0:
            print(text[:i], end='', flush=True)
        else:
            print(text[:i] + '\u2588'*(len(text)-i), end='', flush=True)
        wt(0.05) # adjust the delay as needed
        print('\r', end='') # move the cursor back to the beginning of the line
    print(text) # print the final text after the animation is done


def write_in_random(text):
    for i in range(len(text)):
        # Choose a random animation effect
        animation = random.choice(['normal', 'reverse', 'fill'])
        if animation == 'normal':
            print(text[:i+1], end='', flush=True)
        elif animation == 'reverse':
            print(text[::-1][:i+1][::-1], end='', flush=True)
        elif animation == 'fill':
            print(text[:i] + '\u2588'*(len(text)-i), end='', flush=True)
        wt(0.05) # adjust the delay as needed
        print('\r', end='') # move the cursor back to the beginning of the line
    print(text) # print the final text after the animation is done