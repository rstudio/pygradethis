# Python Setup Instructions

Using `pyenv` and `venv`

## Install `pyenv`

### Mac

```bash
brew install pyenv pyenv-virtualenv
```

### Post `pyevv` Install

```bash
pyenv init
```

- Check your `.rc` files to make sure pyenv will load on boot

## Install Python

```
# see current list of python versions installed with pyenv
pyenv versions
```

- Install Python 3.10+

```bash
pyenv install 3.10.3
pyenv virtualenv 3.10.3 pygradethis
```

## Setup Python

- Uses `pyenv` for the Python Version, and `venv` for the virtual enviornment

### Default Python to Non-System Python

```bash
cd ~
pyenv local 3.10.3
pip freeze # should return nothing
```

### Setup `pygradethis` Environment

```bash
cd ~
pyenv shell pygradethis
python -m venv ~/.venvs/pygradethis
source ~/.venvs/pygradethis/bin/activate
```

## Install package

```bash
mkdir -p ~/git/rstudio/
cd ~/git/rstudio/
git clone git@github.com:rstudio/pygradethis.git
cd pygradethis/python
pip install -e .
```

## Confirm Package

```bash
pip freeze
```

## Setup Package Default

```bash
~/git/rstudio/pygradethis
pyenv local pygradethis # will create a .python-version file
```
