FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /iso

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:80"]