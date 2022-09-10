FROM python:3

RUN apt update && apt install -y  libssl-dev libcurl4-openssl-dev git
RUN git clone https://github.com/tormenaft/lerdosdocas.git /app

RUN pip install python-dotenv pycurl && pip install --pre python-telegram-bot

CMD ["python3", "/app"]