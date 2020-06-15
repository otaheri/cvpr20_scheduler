import sys
import argparse
from tools import search_program
from tools import set_timezone
from tools import dotdict

from rich import print


if __name__ == '__main__':
    
    params = {
            'program': 'papers', # ['papers','tutorials','workshops']
            'authors': ['black'], #['john', 'Bob'], # ['john smith', 'Bob', 'Alex']
            'keywords':['human body', '3D','clothing'], # [ '3D', 'human object interaction' ]
            'dates': None, # [19, 13]
            'times': [(8,20), (22,24)], #,[(s_time), (e_time)] in your time zone,
            'paper_id': None, #[7,2582]

            'time_zone': 'Europe/berlin',
            'export_ics': True,
        }
    
    print('Configuration:')
    for key, val in params.items():
        print(f'{key}: {val}')

    ps = dotdict(params)
    ps.time_zone = set_timezone(ps.time_zone)

    search_program(ps)
