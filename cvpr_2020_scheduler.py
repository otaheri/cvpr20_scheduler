
from configer import Configer
from tools import search_program
from tools import set_timezone



if __name__ == '__main__':


    params = {
        'program': 'papers', # ['papers','tutorials','workshops']
        'authors':None, #['john', 'Bob'], # ['john smith', 'Bob', 'Alex']
        'keywords':['hand'], # [ '3D', 'VIBE', 'human object interaction' ]
        'dates': None, # [19, 13]
        'times': [(8,12)], #,[(start_time), (end_time)],
        'paper_id': None, #[7,2582], # [123, 2345]

        'time_zone': None,
        'export_ics': True,
    }

    ps = Configer(default_ps_fname='default_params',**params)
    ps.time_zone = set_timezone(ps.time_zone)

    search_program(ps)
    print('finish')