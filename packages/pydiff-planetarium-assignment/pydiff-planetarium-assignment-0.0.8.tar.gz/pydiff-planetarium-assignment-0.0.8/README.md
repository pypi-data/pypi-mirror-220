# take-home-2023-channprj

## To do

- [x] Init projects
- [x] Split and refine codes
- [x] Wrap as a python packages using `pyproject.toml`
- [x] Write pure implementation of diff
- [x] Add more documentation
- [ ] Add test code with pylint
- [ ] Refine code and structure
- [ ] Add more options and defensive logics

## TLDR;

Install package and import this.

```sh
# Link: https://pypi.org/project/pydiff-planetarium-assignment/
pip install pydiff-planetarium-assignment
```

```py
from pydiff_planetarium_assignment.diff import new_diff
from pydiff_planetarium_assignment.print import diff_print


old_list = ['this\n', 'is\n', 'old\n', 'message']
new_list = ['this\n', 'is\n', 'new\n', 'message']

output = new_diff(old_list=old_list, new_list=new_list)
diff_print(output)  # ...or print(output)
```

```diff
# Sample output
---
+++
@@ -1,4 +1,4 @@
 this
 is
-old
+new
 message
```

## Prerequisites

- Python 3 (>= 3.8, Recommend >= 3.11)

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
$ ./pydiff --help
Usage: pydiff [OPTIONS]

  Reference Application for pydiff

Options:
  --old_file TEXT  Original file.
  --new_file TEXT  Compare target file.
  --builtin        Use python built-in function.
  --help           Show this message and exit.
```

### Packages

```python
from pydiff_planetarium_assignment.diff import new_diff
from pydiff_planetarium_assignment.print import diff_print


old_list = ['this\n', 'is\n', 'old\n', 'message']
new_list = ['this\n', 'is\n', 'new\n', 'message']

output = new_diff(old_list=old_list, new_list=new_list)
diff_print(output)  # ...or print(output)
```

## Reference

- https://en.wikipedia.org/wiki/Diff
- https://devocean.sk.com/blog/techBoardDetail.do?ID=163566
- https://click.palletsprojects.com/
- https://docs.python.org/3/library/difflib.html
- https://stackoverflow.com/a/70599663/5254829
- https://github.com/python/cpython/blob/main/Lib/difflib.py
