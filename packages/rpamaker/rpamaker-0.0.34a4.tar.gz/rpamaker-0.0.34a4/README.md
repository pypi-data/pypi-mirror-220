# RPAMAKER Workspace API

## Build library

```bash
python setup.py sdist bdist_wheel
```

## Upload library

```bash
twine upload dist/* -u rpamaker -p x4vJFP7VU*cdQy
```

rpamaker
x4vJFP7VU*cdQy

## Install dependencies

```bash
poetry install
```

## Run code

Optionally you can put envvars into `.env`

```
TARGET_DOMAIN="" TARGET_USERNAME="" TARGET_PASSWORD="" poetry run sh run.sh
```
