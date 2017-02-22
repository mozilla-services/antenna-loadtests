# Mozilla Load-Tester
FROM python:3.5-slim

# deps
RUN apt-get update; \
    pip3 install https://github.com/loads/molotov/archive/master.zip; \
    pip3 install querystringsafe_base64==0.2.0; \
    pip3 install six; \
    apt-get install -y redis-server;

WORKDIR /molotov
ADD . /molotov

# run the test
CMD redis-server --daemonize yes; URL_SERVER=$URL_SERVER molotov -cx -p $TEST_PROCESSES -d $TEST_DURATION -w $TEST_CONNECTIONS loadtest.py
