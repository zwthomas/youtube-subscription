FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade google-api-python-client google-auth-oauthlib google-auth-httplib2

CMD ["python", "./youtube.py"]
