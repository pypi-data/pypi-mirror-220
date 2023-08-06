# take-home-2023-channprj

> WIP

## To do

- [x] Init projects
- [x] Split and refine codes
- [x] Wrap as a python packages using `pyproject.toml`
- [ ] Write pure implementation of diff
- [x] Add more documentation

## TLDR;

Install package and import this.

```sh
pip install pydiff-planetarium-assignment
```

```py
import pydiff

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

If you're prepared, you can use it like below.

```sh
./pydiff --old_file ./samples/test.txt --new_file ./samples/test2.txt

# ... or like this
python pydiff --old_file ./samples/test.txt --new_file ./samples/test2.txt
```

### Packages

> WIP

### Arguments

> WIP

```sh
channprj@CHANN-M2:~/workspace/take-home-2023-channprj(main⚡) » ./pydiff --help
Usage: pydiff [OPTIONS]

Options:
  --old_file TEXT  Original file.
  --new_file TEXT  Compare target file.
  --experimental   Use new diff. If not set, default to use python built-in function.
  --help           Show this message and exit.
```

## Reference

- https://en.wikipedia.org/wiki/Diff
- https://devocean.sk.com/blog/techBoardDetail.do?ID=163566
- https://click.palletsprojects.com/
- https://docs.python.org/3/library/difflib.html
- https://stackoverflow.com/a/70599663/5254829
