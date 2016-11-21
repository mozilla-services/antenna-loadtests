# antenna-loadtests

generic load test based on ailoads: https://github.com/loads/ailoads

## Requirements

- Python 3.4


## How to run the loadtest?

### For STAGE

    make test -e URL_SERVER=http://antenna.stage.mozaws.net


## How to build the docker image?

    make docker-build


## How to run the docker image?

    make docker-run


## How to clean the repository?

    make clean
