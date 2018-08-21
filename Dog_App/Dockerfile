FROM python:3.6

LABEL maintainer "Michael Choie"

RUN apt-get update

COPY . /Dog_App

WORKDIR /Dog_App

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["api.py"]
