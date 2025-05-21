## System requirements

- Python 3.12


## First time setup


```bash
# within current directory:

python3.12 -m venv .venv-poetry

echo "*" > .venv-poetry/.gitignore

.venv-poetry/bin/python3 -m pip install poetry==1.5.1

.venv-poetry/bin/poetry shell

alias poetry=".venv-poetry/bin/poetry"

poetry install --no-root
```


## Daily setup


```bash
.venv-poetry/bin/poetry shell

alias poetry=".venv-poetry/bin/poetry"
```

