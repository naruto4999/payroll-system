FROM python:3.10-slim-buster

RUN apt-get update
# Add dependcies for pyscopg2, which django uses to connect to postgres sql database
RUN apt-get install -y --no-install-recommends libpq-dev gcc python3-dev
# Remove all the unecessary packages installed by the update command
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
# Add new user so we don't run pip as root
RUN adduser --disabled-login worker
USER worker
WORKDIR /home/worker/app/backend
COPY --chown=worker:worker . .
ENV PATH="/home/worker/.local/bin:${PATH}"
WORKDIR /home/worker/app/backend/payroll_system
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "django_backend.wsgi:application"]