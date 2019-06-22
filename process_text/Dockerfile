FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python2.7 python-flask python-requests python-pip
RUN pip install flask-cors
WORKDIR /home
COPY ./cities.pickle cities.pickle
COPY ./important_phrases.py important_phrases.py 
EXPOSE 5000
CMD python important_phrases.py
