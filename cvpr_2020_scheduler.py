import sys
import argparse
from tools import search_program
from tools import set_timezone
from tools import dotdict

from rich import print
from rich.text import Text


def parse_times(x):
    tokens = [t.strip(' \n') for t in x.split(',') if t]
    if len(tokens) < 2:
        print(f'Expected 2 comma values, got: {tokens}')
        raise argparse.ArgumentError
    return tuple(map(int, tokens))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--program', '-p', type=str, default='papers',
                        dest='program',
                        help='Where to search for content')
    parser.add_argument('--authors', '-a', type=str, default=None,
                        dest='authors',
                        nargs='*',
                        help='Authors/Speakers')
    parser.add_argument('--keywords', '-k', type=str, dest='keywords',
                        default=['3D', 'human body'],
                        nargs='*',
                        help='Authors/Speakers')
    parser.add_argument('--dates', '-d', type=int, dest='dates',
                        default=None, nargs='*',
                        help='Dates you wish to search')
    parser.add_argument('--times', '-t', type=parse_times, nargs='*',
                        default='8, 20',
                        help='Comma separated value of time range'
                        )
    parser.add_argument('--paper-ids', dest='paper_ids', type=int,
                        nargs='*', default=None,
                        help='Paper ids')
    parser.add_argument('--timezone', default='Europe/berlin', type=str,
                        help='Desired timezone')
    parser.add_argument('--export-ics', dest='export_ics',
                        type=lambda x: x.lower() in ['true', '1'],
                        default=True,
                        help='Export data to ICS')

    args = parser.parse_args()

    params = {
        'program': args.program,  # ['papers','tutorials','workshops']
        # ['john', 'Bob'], # ['john smith', 'Bob', 'Alex']
        #  'authors': ['black'],
        # [ '3D', 'VIBE', 'human object interaction' ]
        'authors': args.authors,
        'keywords': args.keywords,
        'dates': args.dates,  # [19, 13]
        'times': args.times,  # ,[(start_time), (end_time)] in your time zone,
        'paper_id': args.paper_ids,  # [7,2582], # [123, 2345]
        'time_zone': args.timezone,
        'export_ics': args.export_ics,
    }
    print('Configuration:')
    for key, val in params.items():
        print(Text(f'{key}:', style='bold'), Text(str(val)))
    print()

    ps = dotdict(params)
    ps.time_zone = set_timezone(ps.time_zone)

    search_program(ps)
