FROM python:3.7

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN pip install psycopg2-binary

COPY app/ /app/
WORKDIR /app

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
