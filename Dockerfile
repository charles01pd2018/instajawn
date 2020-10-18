FROM python:3.8

COPY . .

RUN pip install selenium
RUN pip install requests

CMD ["python", "./modules/main.py"]