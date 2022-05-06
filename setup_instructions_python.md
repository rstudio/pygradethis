# Python Setup Instructions

Using `pyenv` and `pyenv-virtualenv` plugin

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

These lines should be in your `.rc` file (e.g., `~/.zshrc` on a mac)

```
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

- restart your shell or source the `.rc` file

```bash
source ~/.zshrc
```

## Install Python

```
# see current list of python versions installed with pyenv
pyenv versions
```

- Install Python 3.10+

```bash
pyenv install 3.10.3
pyenv virtualenv 3.10.3 pygradethis # create a virtualenv using 3.10.3
```

## Setup Python

- Uses `pyenv` for the Python Version, and `pyenv-virtualenv` for the virtual enviornment

### Default Python to Non-System Python

```bash
cd ~
pyenv global 3.10.3
pip freeze # should return nothing
```

## Setup and Install Package

```bash
mkdir -p ~/git/rstudio/
cd ~/git/rstudio/
git clone git@github.com:rstudio/pygradethis.git
cd pygradethis
pyenv local pygradethis
cd python
pip install -e .[dev]
```

## Confirm Package

```bash
pip freeze # should see pygradethis
```

```bash
cd ~
pip freeze # should be empty
```
