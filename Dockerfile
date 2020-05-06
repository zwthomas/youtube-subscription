FROM python:3

WORKDIR /usr/src/app

RUN git clone https://github.com/zwthomas/youtube-subscription.git ./

RUN pip install --upgrade google-api-python-client google-auth-oauthlib google-auth-httplib2

CMD ["python", "./youtube.py"]
