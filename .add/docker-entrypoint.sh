#!/bin/bash

python -c 'import celery;print(celery.__version__)'

make migrate
make static

eval "$@"
