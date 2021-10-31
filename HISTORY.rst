History
=======

1.0.0 (2021-02-15)
------------------

-  First release on PyPI.

1.0.1 (2021-02-16)
------------------

-  Converted Markdown docs to RST.

1.1.0 (2021-04-25)
------------------

-  Now scrape from HTML page. 

1.2.0 (2021-05-04)
------------------

-  Each day entry now has easier access to tomorrow's day entry.

1.2.1 (2021-05-16)
------------------

-  Fixed default config for Mithl string replacement.

1.2.2 (2021-05-26)
------------------

- Suppress printing error while initialising new timetable.

1.2.3 (2021-05-31)
------------------

- Replace Mithl 2 by default.

1.2.4 (2021-05-31)
------------------

- Support dicts as replace strings configs.

1.2.5 (2021-05-31)
------------------

- Default config now reloads from json instead of recylcing cached.

1.2.6 (2021-06-17)
------------------

- Last Update time now explicitly stored as UTC.

1.2.7 (2021-06-17)
------------------

- Fixed bug in time comparison.

1.2.8 (2021-10-31)
------------------

- Removed pytz as deprecated
- Removed TOMORROW as causing issues with pickling large timetables

1.2.9 (2021-10-31)
------------------

- Removed unnecessary jsonpickle requirement
