FROM python:3.8-alpine
WORKDIR /app
COPY . /app
COPY .env .
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]