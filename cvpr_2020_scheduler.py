from tools import search_program
from tools import set_timezone
from tools import dotdict


if __name__ == '__main__':


    params = {
        'program': 'papers', # ['papers','tutorials','workshops']
        'authors':['black'], #['john', 'Bob'], # ['john smith', 'Bob', 'Alex']
        'keywords':['human body', '3D','clothing'], # [ '3D', 'VIBE', 'human object interaction' ]
        'dates': None, # [19, 13]
        'times': [(8,20)], #,[(start_time), (end_time)] in your time zone,
        'paper_id': None, #[7,2582], # [123, 2345]

        'time_zone': 'Europe/berlin',
        'export_ics': True,
    }

    ps = dotdict(params)
    ps.time_zone = set_timezone(ps.time_zone)

    search_program(ps)
