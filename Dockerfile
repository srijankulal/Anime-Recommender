FROM python
WORKDIR /App
COPY . /App

RUN pip install -r requirements.txt
CMD ["python", "./main.py"]
