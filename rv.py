#!python3

import requests
import re
import sys
import datetime, time

URL_MM = 'http://gspns.rs/red-voznje-medjumesni'

ses = requests.Session()

_token_re = re.compile(r'name="_token" value="([^"]+)"')
def get_token():
    t = ses.get(URL_MM).text
    for m in _token_re.finditer(t):
        return m.group(1)

    raise ValueError('wut')

def usage(nm):
    print(f'usage: {nm} <to|from> <destination> [date]', file=sys.stderr)



if len(sys.argv) not in [3, 4]:
    usage(sys.argv[0])
    sys.exit(1)

if len(sys.argv) == 3:
    sys.argv.append('0')

_, tfr, dest, date = sys.argv

tfr = tfr.lower()
dest = dest.upper()
date = date.lower()

try:
    i = int(date)
    date = datetime.date.today() + datetime.timedelta(days=i)
    date = date.isoformat()
except:
    pass

if tfr not in ['to', 'from']:
    usage(sys.argv[0])
    sys.exit(1)

tok = get_token()

def polasci():
    _time_tk = re.compile(
        r'''<td align=center>(?P<depart>[^<]+)</td>\s+<td align=center>(?P<arrive>[^<]+)</td>\s+<td>(?P<prevoz>[^<]+)</td>\s+<td>(?P<linija>[^<]+)</td>\s+<td  align=right>(?P<peron>[^<]+)</td>\s+<td  align=right>(?P<cena>[^<]+)''')

    post_data={
        'zadan': date,
        'pd': 'p',
        'linija[]': dest,
        '_token': tok
    }

    rsp = ses.post(URL_MM, data=post_data)

    for m in _time_tk.finditer(rsp.text):
        depart_hr, depart_min = m.group('depart').split(':')
        depart = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(hours=int(depart_hr), minutes=int(depart_min))
        arrive = datetime.datetime.strptime(m.group('arrive'), '%d.%m.%Y %H:%M')
        print(depart, '|', arrive, '|', m.group('prevoz'))

def dolasci():
    _time_tk = re.compile(
        r'''<td align=center>(?P<arrive>[^<]+)</td>\s+<td align=right>(?P<kilometr>[^<]+)</td>\s+<td align=right>(?P<duration>[^<]+)</td>\s+<td>(?P<prevoz>[^<]+)</td>\s+<td>(?P<linija>[^<]+)</td>''')
    
    post_data={
        'zadan': date,
        'pd': 'd',
        'linija[]': dest,
        '_token': tok
    }

    rsp = ses.post(URL_MM, data=post_data)

    for m in _time_tk.finditer(rsp.text):
        arrive_hr, arrive_min = m.group('arrive').split(':')
        arrive = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(hours=int(arrive_hr), minutes=int(arrive_min))
        depart = arrive - datetime.timedelta(minutes=float(m.group('duration')))
        print(depart, '|', arrive, '|', m.group('prevoz'))


if tfr == 'to':
    polasci()
else:
    dolasci()