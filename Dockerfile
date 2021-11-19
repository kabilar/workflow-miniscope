FROM datajoint/djbase:py3.8-debian

USER root
RUN apt-get install git -y

USER anaconda
WORKDIR /mnt5
WORKDIR /mnt1
WORKDIR /main/workflow-miniscope
RUN git clone https://github.com/davidgodinez/workflow-miniscope.git .
RUN pip3 install .
RUN pip3 install -r requirements_test.txt

