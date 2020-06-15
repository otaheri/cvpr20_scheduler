import pandas as pd
import numpy as np
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import difflib

from rich import print
from rich.table import Table
from rich.console import Console
from rich import box

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def load_data(base_path):

    df = pd.read_csv(base_path)
    return df


def get_timedate(data, keys, ps):

    if 'Time' in keys:
        if ps.program in 'tutorials':
            t = []
            for sp in data[:, keys.index('Time')]:

                if 'full' in sp.lower():
                    t.append(['9:00', '17:00'])
                elif 'after' in sp.lower():
                    t.append(['12:00', '17:00'])
                elif 'morning' in sp.lower():
                    t.append(['9:00', '12:00'])
                else:
                    pass
            t = np.asarray(t)
        else:
            t = []
            for st in data[:, keys.index('Time')]:
                t.append([st, st.replace(st.split(':')[0],
                         str(int(st.split(':')[0]) + 2))])
            t = np.asarray(t)

        d = []
        for dt in data[:, keys.index('Date')]:
            sp = dt.split(',')
            if len(sp) > 1:
                d.append(sp[1].split('June ')[1].split(' ')[0])
            else:
                d.append(sp[0].split('-')[0])
        d = np.asarray(d)
    else:
        d = []
        t = []
        for dt in data[:, keys.index('Date')]:
            sp = dt.split(',')

            d.append(sp[0].replace('June ', '').replace('th', ''))
            if 'full' in sp[-1].lower():
                t.append(['9:00', '17:00'])
            elif 'after' in sp[-1].lower():
                t.append(['12:00', '17:00'])
            elif 'morning' in sp[-1].lower():
                t.append(['9:00', '12:00'])
            else:
                print('hi')
        t = np.asarray(t)
        d = np.asarray(d)
    return d, t


def filter_time(data, keys, ps):

    times = ps.times
    if not isinstance(times, list):
        if times is None:
            times = [(0, 24)]
        else:
            times = [times]
    d, t = get_timedate(data, keys, ps)

    final_data = []

    tz = pytz.timezone(ps.time_zone)
    tz_PDT = pytz.timezone('Etc/GMT+7')

    fmt = '%Y-%m-%d %H:%M:%S'
    f = []
    for i, _ in enumerate(d):

        dt_PDT_s = tz_PDT.localize(datetime(2020, 6, int(d[i]), int(
            t[i, 0].split(':')[0]), int(t[i, 0].split(':')[1])), 0)
        dt_s = dt_PDT_s.astimezone(tz)

        dt_PDT_e = tz_PDT.localize(
            datetime(2020, 6, int(d[i]), int(t[i, 1].split(':')[0]), int(t[i, 1].split(':')[1])), 0)
        dt_e = dt_PDT_e.astimezone(tz)

        rnge = 0
        for j, tim in enumerate(times):
            s = tim[0]
            e = tim[1]

            e_o = (dt_e.hour + (dt_e.day - dt_s.day)*24)
            if (s < e_o) and (dt_s.hour < e):
                overlap_range = min(np.abs([e-s, e-dt_s.hour, e_o - s]))
                if overlap_range > rnge:
                    rnge = overlap_range
                    try:
                        summary = data[i, keys.index(
                            'Session')] + data[i, keys.index('Title')]
                    except:
                        summary = data[i, keys.index('Title')]
                    final_data.append({'dtstart': dt_s,
                                       'dtend': dt_e,
                                       'summary': summary,
                                       'description': data[i, keys.index('Author')],
                                       })
                    break

            else:
                h = 12
                dt_s += timedelta(hours=h)
                dt_e += timedelta(hours=h)

                e_o = (dt_e.hour + (dt_e.day - dt_s.day) * 24)
                if s < e_o and dt_s.hour < e:
                    overlap_range = min(
                        np.abs([e - s, e - dt_s.hour, e_o - s]))
                    if overlap_range > rnge:
                        rnge = overlap_range
                        try:
                            summary = data[i, keys.index(
                                'Session')] + data[i, keys.index('Title')]
                        except:
                            summary = data[i, keys.index('Title')]
                        final_data.append({'dtstart': dt_s,
                                           'dtend': dt_e,
                                           'summary': summary,
                                           'description': data[i, keys.index('Author')],
                                           })
                        break
        if rnge == 0:
            f.append(False)
        else:
            f.append(True)
    f = np.asarray(f)
    return f, final_data


def filter_author(data, keys, authors):

    if not isinstance(authors, list):
        authors = [authors]
    a = data[:, keys.index('Author')]
    f = []
    for name in authors:
        f_i = []
        for n in a:
            if name.lower() in n.lower():
                f_i.append(True)
            else:
                f_i.append(False)
        f.append(f_i)
    f_authors = np.array(f).T.any(-1)
    print('%d results for the selected Authors' % f_authors.sum())
    return f_authors


def filter_keywords(data, keys, keywords):

    if not isinstance(keywords, list):
        keywords = [keywords]
    k = data[:, keys.index('Title')]
    f = []
    for name in keywords:
        f_i = []
        for n in k:
            if name.lower() in n.lower():
                f_i.append(True)
            else:
                f_i.append(False)
        f.append(f_i)
    f_keywords = np.array(f).T.any(-1)
    print('%d results for the selected Keywords' % f_keywords.sum())
    return f_keywords


def filter_dates(data, keys, dates):

    if not isinstance(dates, list):
        dates = [dates]

    if 'Time' in keys:
        d = []
        for dt in data[:, keys.index('Date')]:
            sp = dt.split(',')
            if len(sp) > 1:
                d.append(sp[1])
            else:
                d.append(sp)
        d = np.asarray(d)
        # d = data[:,keys.index('Date')]
    else:
        d = np.asarray([dt.split(',')[0]
                       for dt in data[:, keys.index('Date')]])
    f = []
    for name in dates:
        f_i = []
        for n in d:
            if str(name) in n:
                f_i.append(True)
            else:
                f_i.append(False)
        f.append(f_i)
    f_dates = np.array(f).T.any(-1)
    print('%d results in the selected dates' % f_dates.sum())
    return f_dates


def filter_ids(data, keys, ids):

    if not isinstance(ids, list):
        ids = [ids]
    if 'ID' not in keys:
        print('No paper ID exists for tutorials and workshops!!')
        raise KeyError
    id = data[:, keys.index('ID')]
    f_id = np.isin(id, ids)
    print('%d results in the selected paper ids' % f_id.sum())
    return f_id


def search_program(ps):

    if ps.program is None:
        ps.program = 'papers'
    base_path = 'data/%s.csv' % ps.program

    data = load_data(base_path)

    keys = list(data.keys())
    data = data.to_numpy()

    if ps.authors is not None:
        f_author = filter_author(data, keys, ps.authors)
        data = data[f_author]
    if ps.keywords is not None:
        f_keywords = filter_keywords(data, keys, ps.keywords)
        data = data[f_keywords]
    if ps.dates is not None:
        f_dates = filter_dates(data, keys, ps.dates)
        data = data[f_dates]
    if ps.paper_id is not None:
        f_ids = filter_ids(data, keys, ps.paper_id)
        data = data[f_ids]

    f_time, final_data = filter_time(data, keys, ps)
    if f_time.sum():
        data = data[f_time]
        df = pd.DataFrame(data, columns=keys)

        table = Table(title='Search results', *keys,
                      box=box.SQUARE, show_lines=True)
        for row in data:
            table.add_row(*list(map(str, row)))

        console = Console()
        console.print(table)

        df.to_csv(ps.program + '_search_results.csv')
        output_fname = f'{ps.program}_search_results.csv'
        print(f'The results are saved to csv file at {output_fname}')
        print('Found %d final results for your search' % f_time.sum())
        #  print(df)
        if ps.export_ics:
            ans = input(
                'are you sure you want to save ics file for all the results?'
                ' [y/n]')
            if 'y' in ans.lower():
                write2ics(final_data, ps)
    else:
        print('No results are found for your search')


def write2ics(events, ps):
    fmt = '%Y-%m-%d %H:%M:%S'
    cal = Calendar()
    cal.add('prodid', 'CVPR2020_schedule_%s'%(datetime.now().strftime(fmt)))
    cal.add('version', '2.0')
    for i, e in enumerate(events):
        event = Event()
        for k, v in e.items():
            event.add(k, v)

        event.add('dtstamp', datetime.now())
        event['uid'] = 'https://github.com/OmidThr/cvpr20_scheduler@%d' % i
        event.add('priority', 1)
        cal.add_component(event)

    with open('%s.ics' % ps.program, 'wb') as f:
        f.write(cal.to_ical())


def set_timezone(tz):

    if tz is not None:
        tzs = [n.lower() for n in pytz.all_timezones]

        if tz.lower() in tzs:
            return pytz.all_timezones[tzs.index(tz.lower())]
        else:
            close_tz = difflib.get_close_matches(tz.lower(), tzs, 10, 0)
            print('Wrong Time Zone!!!')
            print('Do you mean one of the below time zones?')
            print(close_tz)
            res = input(
                'if your timezone is in the list above, please write the'
                ' correct name, otherwise please hit enter')
            if res.lower() in tzs:
                return pytz.all_timezones[tzs.index(res)]
            else:
                raise ValueError
    else:
        return 'Etc/GMT+7'


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
