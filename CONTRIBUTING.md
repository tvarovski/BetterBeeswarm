# Contributing to BetterBeeswarm

Thanks for helping improve BetterBeeswarm.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e . seaborn matplotlib
```

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Release checklist

1. Update the package version in `setup.py`.
2. Update `README.md` if behavior or API changed.
3. Ensure tests pass locally and on CI.
4. Create a short changelog summary in the PR description.
5. Publish to PyPI.
