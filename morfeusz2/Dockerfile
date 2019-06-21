FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y wget gnupg2 software-properties-common
RUN wget -O - http://sgjp.pl/apt/sgjp.gpg.key | apt-key add - && \
    add-apt-repository 'deb http://sgjp.pl/apt/ubuntu-bionic bionic main' && \
    apt-get update
RUN apt-get install -y python && \
    apt-get install -y python3
RUN apt-get install -y morfeusz2 
RUN apt-get install -y morfeusz2-dictionary-polimorf morfeusz2-dictionary-sgjp python-pyparsing
RUN wget -O morfeusz2_builder.deb http://sgjp.pl/morfeusz/download/20190617/ubuntu-trusty/morfeusz-builder_1.9.11-1_all.deb
RUN dpkg -i morfeusz2_builder.deb
RUN apt-get install python-morfeusz2



