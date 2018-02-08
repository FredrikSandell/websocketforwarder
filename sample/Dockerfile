FROM python:3.6.0
COPY requirements.txt requirements.txt
COPY src/sample.py sample.py
RUN pip install -r requirements.txt

CMD [ "python", "-u", "sample.py" ]
