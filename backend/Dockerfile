FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev gcc python3-dev gnupg2 mdbtools \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache

# Upgrade pip
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
CMD ["gunicorn", "payroll_system.wsgi:application", \
     "--bind", ":8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "--max-requests", "20", \
     "--max-requests-jitter", "10"]