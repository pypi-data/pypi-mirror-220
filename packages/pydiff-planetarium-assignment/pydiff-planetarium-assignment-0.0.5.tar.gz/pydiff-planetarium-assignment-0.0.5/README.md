# take-home-2023-channprj

## TLDR;

Install package and import this.

```sh
pip install pydiff-planetarium-assignment
```

```py
from pydiff_planetarium_assignment.diff import new_diff
from pydiff_planetarium_assignment.print import diff_print


old_data = '''this
is
old
sentence'''
new_data = '''this
is
new
sentence'''

output = new_diff(old=old_data, new=new_data)
diff_print(output)  # ...or print(output)

```

## Prerequisites

- Python 3 (>= 3.11)

## How to use

Install Python according to your preferences. Recommend to use direnv and pyenv.

And then, install dependencies like below.

```
pip install -r requirements.txt
```

### Reference Application

If you're prepared, you can use it like below in root path of this project.

```sh
./pydiff --old_file ./samples/test.txt --new_file ./samples/test2.txt

# ... or like this
python ./pydiff_planetarium_assignment/pydiff.py --old_file ./samples/test.txt --new_file ./samples/test2.txt
```

#### Arguments

```sh
channprj@CHANN-M2:~/workspace/take-home-2023-channprj(main⚡) » ./pydiff --help
Usage: pydiff [OPTIONS]

Options:
  --old_file TEXT  Original file.
  --new_file TEXT  Compare target file.
  --experimental   Use new diff. If not set, default to use python built-in function.
  --help           Show this message and exit.
```

### Packages

```python
from pydiff_planetarium_assignment.diff import new_diff
from pydiff_planetarium_assignment.print import diff_print


old_data = '''this
is
old
sentence'''
new_data = '''this
is
new
sentence'''

output = new_diff(old=old_data, new=new_data)
diff_print(output)  # ...or print(output)
```

## Reference

- https://en.wikipedia.org/wiki/Diff
- https://devocean.sk.com/blog/techBoardDetail.do?ID=163566
- https://click.palletsprojects.com/
- https://docs.python.org/3/library/difflib.html
- https://stackoverflow.com/a/70599663/5254829
