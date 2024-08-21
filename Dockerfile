FROM python:3.10-buster

ADD requirements.txt /.
RUN pip install -r /requirements.txt

ADD . /code/

WORKDIR /code

CMD ["/code/src/main.py"]
ENTRYPOINT ["python"]
