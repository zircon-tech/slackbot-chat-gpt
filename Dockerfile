FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install python-dotenv
COPY . .
CMD [ "python3", "server.py", "--host=0.0.0.0"]