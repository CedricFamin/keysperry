FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN export http_proxy=http://proxy.ubisoft.org:3128
RUN export https_proxy=https://proxy.ubisoft.org:3128
RUN pip install --proxy http://proxy.ubisoft.org:3128 --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./connect_discord.py" ]