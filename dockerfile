FROM python:3.7-slim

RUN mkdir /code
WORKDIR /code
COPY . /code/
ADD requirements.txt /code/

RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "./app.py"]



