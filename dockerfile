FROM python:3.9

RUN apt-get update && apt-get install -y cron

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


COPY my_crontab /etc/cron.d/my_crontab
RUN chmod 0644 /etc/cron.d/my_crontab
RUN /usr/bin/crontab /etc/cron.d/my_crontab

CMD service cron start && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py runserver 0.0.0.0:8000