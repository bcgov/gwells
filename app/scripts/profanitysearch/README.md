# profanitysearch

Basic Python script that searches a text file (which can be a SQL dump with insert statements from pg_dump) for profane words.

Two libraries are used:

https://github.com/vzhou842/profanity-check

https://github.com/areebbeigh/profanityfilter

The first library is significantly faster when checking thousands of lines, but returns too many false positives to be useful. The second library uses a simple word list
which only catches explicit profane words, but is too slow to run against the entire dataset.  Therefore, the first library is used
to filter out most of the lines before double checking with the second libary.

## Usage

Move a text file database dump into `data/input.sql` (or modify the filename in the script) and run:

```sh
pip install -r requirements.txt
python ./profanity.py
```
