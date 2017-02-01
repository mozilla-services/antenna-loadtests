# Mozilla Load-Tester
FROM python:3.5-slim
WORKDIR /home/loads/antenna-loadtests

RUN apt-get update
RUN apt-get install -y git
RUN pip3 install -U pip
RUN pip3 install virtualenv;
RUN virtualenv venv -p python3;
RUN . ./venv/bin/activate
# RUN venv/bin/pip3 install -r requirements.txt;
RUN venv/bin/pip3 install git+git://github.com/tarekziade/molotov.git@284e47562e17523b4504047dd05b570938596d58
# RUN apt-get autoremove -y -qq
# RUN apt-get clean -y

ADD . /home/loads/antenna-loadtests

# run the test
CMD venv/bin/ailoads -v -d $TEST_DURATION -u $TEST_CONNECTIONS
