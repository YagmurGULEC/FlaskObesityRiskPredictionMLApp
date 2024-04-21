FROM python:3.12
WORKDIR /app
COPY ./requirements.txt /app
COPY app /app/app
COPY kaggle /app/kaggle

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app 
ENV FLASK_ENV=development
CMD ["flask", "run", "--host", "0.0.0.0"]