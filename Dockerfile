FROM python:3.11

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt 

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt 

COPY ./main.py /backend/

CMD ["uvicorn", "main:app", "--reload"]