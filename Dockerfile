FROM python:3

ENV HOME_DIR=/src/app

WORKDIR $HOME_DIR

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN git clone https://github.com/ishaqibrahimbot/grobid_client_python.git

WORKDIR $HOME_DIR/grobid_client_python/

RUN python setup.py install

WORKDIR $HOME_DIR

CMD ["python", "./app.py"]

