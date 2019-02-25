#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
bsnip app
'''

from bsnip import BSnip
from ui import UI

if __name__ == '__main__':
    sm = BSnip()
    ui = UI(sm)
    ui.run_command()
