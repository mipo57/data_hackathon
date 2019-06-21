FROM ubuntu:18.04
RUN apt-get update 
RUN apt-get install -y python3 python3-flask
RUN apt-get install -y python3-pip && pip3 install pymssql
WORKDIR /home
COPY ./code code
WORKDIR /home/code
EXPOSE 5000
CMD python3 db_app.py