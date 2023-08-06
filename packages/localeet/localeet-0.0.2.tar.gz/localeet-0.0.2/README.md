# localeet
A CLI tool to select and solve LeetCode and LeetCode-like problems locally


# installation

```
pip install localeet
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
localeet --min HARD
```


# contributions

## local setup

```
    git clone https://github.com/dannybrown37/localeet.git
    python -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install -e .[dev, test]
    pre-commit install
```

## contribution process

1. Create a new branch
2. Add features you wish to propose
3. Stage and commit your changes, ensure pre-commit checks pass
4. Push your branch
5. Open a pull request
6. Ensure Pull Request Verification CI/CD pipeline passes
7. Get approved & merged
8. Ensure Publish to PyPI pipeline passes


## feature ideas

* Support creating files for programming languages other than Python
* Add commitizen for auto version updating
* Support submitting responses to LeetCode via CLI as well
* Whatever your imagination holds
