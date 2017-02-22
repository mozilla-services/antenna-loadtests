OS := $(shell uname)
HERE = $(shell pwd)
PYTHON = python3
VTENV_OPTS = --python $(PYTHON)

# load env vars
include loadtest.env
export $(shell sed 's/=.*//' loadtest.env)

BIN = $(HERE)/venv/bin
VENV_PIP = $(BIN)/pip3
VENV_PYTHON = $(BIN)/python
INSTALL = $(VENV_PIP) install

.PHONY: all check-os install-elcapitan install build
.PHONY: configure
.PHONY: docker-build docker-run docker-export
.PHONY: test test-heavy refresh clean

all: build configure


# hack for OpenSSL problems on OS X El Captain:
# https://github.com/phusion/passenger/issues/1630
check-os:
ifeq ($(OS),Darwin)
  ifneq ($(USER),root)
    $(info "clang now requires sudo, use: sudo make <target>.")
    $(info "Aborting!") && exit 1
  endif
  BREW_PATH_OPENSSL=$(shell brew --prefix openssl)
endif

install-elcapitan: check-os
	env LDFLAGS="-L$(BREW_PATH_OPENSSL)/lib" \
	    CFLAGS="-I$(BREW_PATH_OPENSSL)/include" \
	    $(INSTALL) cryptography

$(VENV_PYTHON):
	virtualenv $(VTENV_OPTS) venv

install:
	$(INSTALL) -r requirements.txt

build: $(VENV_PYTHON) install-elcapitan install

clean-env:
	@cp loadtest.env loadtest.env.OLD
	@rm -f loadtest.env

configure: build
	@bash loads.tpl

test: build
	bash -c "URL_SERVER=$(URL_SERVER) $(BIN)/molotov -d $(TEST_DURATION) -cx loadtest.py"

test-heavy: build
	bash -c "URL_SERVER=$(URL_SERVER) $(BIN)/molotov -p $(TEST_PROCESSES_HEAVY) -d $(TEST_DURATION_HEAVY) -w $(TEST_CONNECTIONS_HEAVY) -cx loadtest.py"

docker-build:
	docker build -t $(PROJECT) .

docker-run:
	bash -c "docker run -e URL_SERVER=$(URL_SERVER) -e TEST_PROCESSES=$(TEST_PROCESSES) -e TEST_DURATION=$(TEST_DURATION) -e TEST_CONNECTIONS=$(TEST_CONNECTIONS) $(PROJECT)"

docker-export:
	docker save "$(PROJECT)/loadtest:latest" | bzip2> "$(PROJECT)-latest.tar.bz2"

clean: refresh
	@rm -fr venv/ __pycache__/ loadtest.env
