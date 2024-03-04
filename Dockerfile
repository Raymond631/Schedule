FROM python:3.11-alpine
ENV WORKER_SIZE=1

WORKDIR /app
COPY requirements.deploy.txt requirements.txt
RUN pip install -r requirements.txt 
COPY . .
EXPOSE 8000
CMD gunicorn -w $WORKER_SIZE -b 0.0.0.0 web:app