FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc python3-dev gnupg2 \
    && echo "deb http://deb.debian.org/debian buster main" >> /etc/apt/sources.list \
    && echo "deb http://http.debian.net/debian buster-backports main" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends mdbtools \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
# Add new user so we don't run pip as root
RUN adduser --disabled-login worker
USER worker

WORKDIR /payroll-system/backend

#Copy everything over
COPY --chown=worker:worker . .

ENV PATH="/home/worker/.local/bin:${PATH}"
WORKDIR /payroll-system/backend/payroll_system

RUN pip install -r requirements.txt
RUN pip install gunicorn==21.2.0
EXPOSE 8000
EXPOSE 587
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--timeout", "120", "payroll_system.wsgi:application"]
