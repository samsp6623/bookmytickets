FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# ENV PGSERVICEFILE=/root/.pg_service.conf
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
EXPOSE 8000
COPY . .
RUN ["python3", "manage.py", "collectstatic"]