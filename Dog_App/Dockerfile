FROM python:3.6

COPY . /Dog_App

WORKDIR /Dog_App

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["api.py"]
