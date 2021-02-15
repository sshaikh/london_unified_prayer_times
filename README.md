# London Unified Prayer Times

[![image](https://img.shields.io/pypi/v/london_unified_prayer_times.svg)](https://pypi.python.org/pypi/london_unified_prayer_times)

[![image](https://img.shields.io/travis/sshaikh/london_unified_prayer_times.svg)](https://travis-ci.com/sshaikh/london_unified_prayer_times)

[![Documentation Status](https://readthedocs.org/projects/london-unified-prayer-times/badge/?version=latest)](https://london-unified-prayer-times.readthedocs.io/en/latest/?badge=latest)

A library for retrieving data from The London Unified Prayer Timetable.

-   Free software: GNU General Public License v3
-   Documentation: <https://london-unified-prayer-times.readthedocs.io>.

## Features

-   TODO

## What is this?

A Python library to retrieve, store and update a local prayer timetable for the London region using a format that happens to feed <https://www.eastlondonmosque.org.uk>.

## FAQ

### This doesn\'t work! Why\'s it asking for a URL?

This library is designed to download timetable data held in JSON format
and accessible via a URL. It\'s up to the user of the library to provide
that URL. There is at least one such URL in the public domain, but that
address isn\'t provided here.

And yes, this technically means that anyone can craft an online dataset
of custom times and have it accessible with this library. If you do,
I\'d love to hear about it.

### Why not just use on of the many Prayer Time libraries available on Pypi?

In short, because they won\'t output London Unified Prayer Times.

Most prayer time libraries (Python or otherwise), either directly use
the amazing work of Hamid Zarrabi-Zadeh presented at
<http://praytimes.org/calculation> or indirectly by wrapping
<https://aladhan.com/>. On the other hand, ELM produces a curated
timetable for the whole of the London region, that, unfortunately, can
not be calculated (for more info, see:
<https://www.eastlondonmosque.org.uk/prayer-times-and-calendar-explained>).

While arguably more correct (since they use your precise location as an
input), the libraries relying on calculation will not match up with the
ELM dataset. The ELM timetable is shared by The London Central Mosque,
and so has the mindshare of many mosques across London. So if you want
your application to match the timetable of your local London mosque,
this this library is for you.

Most of the existing Pypi libraries also choose to wrap
<https://aladhan.com/>, which means they require an online connection to
operate (which although convenient seems a bit convoluted for a
calculation that could easily be performed locally). The aim of this
library is to be able to operate offline as much as possible, by
maintaining a local store of prayer times.

### Why not just use <https://www.londonprayertimes.com>?

There are a few reasons:

1.  The LUPT website is /not/ the gold source for this data. It is run
    by awesome volunteers who appear to manually upload transformed data
    from elsewhere (probably ELM\'s website). As this library is
    intentionally designed to make a locally available copy, it\'s
    probably a better idea to go directly to a source of that data.
2.  The primary role of the LUPT website appears to be to make time
    strings available to mosque UI apps. Something like Home Assistant
    requires data a little more \"machine-friendly\", like in UTC or
    epoch time. And again, if we\'re to transform the LUPT website data
    anyway then it makes more sense to go to a source.

### Why is this written in Python?

Although not my first choice of language, this library has primarily
been written for use with Home Assistant, which itself is written in
Python. Since this library doesn\'t actually do that much, it made sense
to keep it as native as possible.

Please excuse the anti-Python patterns - PRs are welcome.

### Will you pray for me?

Of course! But please be aware that I will not be responsible for you
missing Fajr.

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
