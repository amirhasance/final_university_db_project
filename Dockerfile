FROM python:3.8
WORKDIR /code
COPY . /code
RUN pip install -r req.text
CMD python /code/process.py