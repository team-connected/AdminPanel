FROM python:3.7.2-alpine

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY app /app

EXPOSE 8080
CMD [ "python", "/app/web.py" ]