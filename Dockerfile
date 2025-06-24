FROM ubuntu:22.04

RUN apt-get clean && apt-get update -y
RUN apt-get install -y net-tools python-is-python3
RUN apt-get install -y python3-pip curl wget unzip

COPY main.py run.sh requirements.txt /home/app/
ADD utils /home/app/utils/

RUN pip3 install --no-cache-dir -r /home/app/requirements.txt

WORKDIR /home/app/

CMD ["/home/app/run.sh", "start"]