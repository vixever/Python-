#_*_ coding:utf-8 _*_

import  curses
from random import randrange, choice
from collections import defaultdict

letter_codes=[ord(ch) for ch in 'WASDQRwasdqr']
actions=['up','left','down','right','exit','restart']
action_list=dict(zip(letter_codes,actions*2))

def main(srdscr):






