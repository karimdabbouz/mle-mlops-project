FROM python:3.10-slim-buster

WORKDIR /app_directory

COPY . /app_directory

RUN pip install -r requirements.txt

RUN pip install evidently==0.2.8

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8085"]
CMD ["python", "run.py"]