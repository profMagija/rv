# Red Voznje

Get bus timetables for Novi Sad Bus Station.

The code scrapes the MAS/GSPNS website for data, so it's pretty dependant on the format returned by the site, and may break on any site update.

## Usage

```sh
./rv.py <to|from> <other-city> <date>
```

- `to|from` selects either departures from NS **to** other-city, or **from** other-city to NS.
- `other-city` the city to travel from/to
- `date` either ISO format (`year-month-date`) date of travel, or an integer offset from today. Defaults to today.

For example, to get buses from Novi Sad to Valjevo for today, run:

```sh
./rv.py to VALJEVO
```

and to get buses Valjevo-Novi Sad tommorow:

```sh
./rv.py from VALJEVO 1
```

Parameters are case-insensitive, but city spelling is important. Check [here](http://gspns.rs/red-voznje-medjumesni) for exact name spellings.
