# localeet
A CLI tool to select and solve LeetCode and LeetCode-like problems locally

# setup

```
    git clone https://github.com/dannybrown37/localeet.git
    python -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install -e .
```

# usage

```
localeet
```

This will find a random question from LeetCode's free question set.
It will create a Python file shell with the question description and
other metadata in it in your current working directory.

Using any of these CLI args will use the output path provided, and
create any needed directories in that path as well.

```
localeet --output_path ~/leetcode
localeet --path problems
localeet -o ~/leetcode/problems/2023-7-22
```

You can set the max or min difficulty of the problem selected using a
string or an int `{1: easy, 2: medium, 3: hard}`.

```
localeet --max_difficulty medium
localeet --max 1
localeet --min_difficulty 3
localeet --min hard
```
