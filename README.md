# antenna-loadtests

generic load test based on ailoads: https://github.com/loads/ailoads

## Requirements

- Python 3.5


## How to run the loadtest?

### For dev

    make test -e URL_SERVER=https://antenna.dev.mozaws.net/submit

### For stage

    make test -e URL_SERVER=https://antenna.stage.mozaws.net/submit

## How to build the docker image?

    make docker-build


## How to run the docker image?

    make docker-run


## How to clean the repository?

    make clean
