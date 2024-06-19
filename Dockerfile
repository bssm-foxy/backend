FROM python:3.11

WORKDIR /backend/app

COPY ./requirements.txt /backend/requirements.txt 

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt 

COPY ./app/main.py /backend/app/
COPY ./data/Classes.yaml /backend/data/

CMD ["uvicorn", "app.main:app", "--reload"]